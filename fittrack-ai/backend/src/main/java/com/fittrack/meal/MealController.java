package com.fittrack.meal;
import java.math.BigDecimal;import java.time.*;import java.time.temporal.ChronoUnit;import java.util.*;import java.nio.charset.StandardCharsets;import java.security.MessageDigest;
import com.fasterxml.jackson.core.type.TypeReference;import com.fasterxml.jackson.databind.ObjectMapper;import com.fittrack.nutrition.Nutrition;import jakarta.validation.Valid;import jakarta.validation.constraints.*;
import org.springframework.jdbc.core.JdbcTemplate;import org.springframework.web.bind.annotation.*;import org.springframework.security.core.annotation.AuthenticationPrincipal;import org.springframework.security.oauth2.jwt.Jwt;import org.springframework.transaction.annotation.Transactional;import org.springframework.web.server.ResponseStatusException;import org.springframework.http.HttpStatus;
@RestController @RequestMapping("/api/v1") public class MealController {
final JdbcTemplate db;final ObjectMapper json;public MealController(JdbcTemplate d,ObjectMapper j){db=d;json=j;}
public record Meal(@NotBlank @Size(max=100) String foodId,@NotNull @DecimalMin("0.1") @DecimalMax("5000") BigDecimal grams,@NotNull @Pattern(regexp="breakfast|lunch|dinner|snack") String mealType,@NotNull OffsetDateTime eatenAt,@NotNull UUID idempotencyKey,@AssertTrue boolean confirmed){}
public record Edit(@NotBlank @Size(max=100) String foodId,@NotNull @DecimalMin("0.1") @DecimalMax("5000") BigDecimal grams,@NotNull @Pattern(regexp="breakfast|lunch|dinner|snack") String mealType,@NotNull OffsetDateTime eatenAt,@AssertTrue boolean confirmed,@NotNull @Min(1) Long version){}
UUID user(Jwt jwt){return UUID.fromString(jwt.getSubject());}
OffsetDateTime timestamp(OffsetDateTime time){return time.withOffsetSameInstant(ZoneOffset.UTC).truncatedTo(ChronoUnit.MICROS);}
String fingerprint(Meal m)throws Exception{return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(json.writeValueAsBytes(List.of(m.foodId(),m.grams().stripTrailingZeros().toPlainString(),m.mealType(),timestamp(m.eatenAt()).toInstant().toString()))));}
String snapshot(String foodId,BigDecimal grams)throws Exception{var foods=db.queryForList("SELECT * FROM foods WHERE id=?",foodId);if(foods.isEmpty())throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Food not found");return json.writeValueAsString(Map.of("food",foods.get(0),"nutrition",Nutrition.calculate(foods.get(0),grams)));}
Map<String,Object> decode(Map<String,Object> row)throws Exception{var out=new LinkedHashMap<>(row);out.put("snapshot",json.readValue(row.get("snapshot").toString(),new TypeReference<Map<String,Object>>(){}));return out;}
@PostMapping("/meals") @ResponseStatus(HttpStatus.CREATED) @Transactional public Object create(@AuthenticationPrincipal Jwt jwt,@Valid @RequestBody Meal m)throws Exception{
 UUID owner=user(jwt);String hash=fingerprint(m);
 // Serialize mutations per user: stable replay records and no concurrent duplicate creations.
 db.queryForObject("SELECT id FROM users WHERE id=? FOR UPDATE",UUID.class,owner);
 var requests=db.queryForList("SELECT * FROM meal_requests WHERE user_id=? AND idempotency_key=?",owner,m.idempotencyKey());
 if(!requests.isEmpty()){var previous=requests.get(0);if(!hash.equals(previous.get("request_hash")))throw new ResponseStatusException(HttpStatus.CONFLICT,"Idempotency key already used for different content");if("null".equals(previous.get("response_json")))throw new ResponseStatusException(HttpStatus.GONE,"This meal was deleted; the original request will not recreate it");return json.readTree(previous.get("response_json").toString());}
 // Old v0.1 entries without a request record must never be duplicated on upgrade.
 var old=db.queryForList("SELECT * FROM meals WHERE user_id=? AND idempotency_key=?",owner,m.idempotencyKey());
 if(!old.isEmpty())throw new ResponseStatusException(HttpStatus.CONFLICT,"Legacy request key already exists; review the existing entry");
 UUID id=UUID.randomUUID();String snap=snapshot(m.foodId(),m.grams());
 db.update("INSERT INTO meals(id,user_id,food_id,grams,meal_type,eaten_at,idempotency_key,snapshot) VALUES(?,?,?,?,?,?,?,?)",id,owner,m.foodId(),m.grams(),m.mealType(),timestamp(m.eatenAt()),m.idempotencyKey(),snap);
 var response=decode(db.queryForMap("SELECT * FROM meals WHERE id=? AND user_id=?",id,owner));
 db.update("INSERT INTO meal_requests(user_id,idempotency_key,request_hash,meal_id,response_json) VALUES(?,?,?,?,?)",owner,m.idempotencyKey(),hash,id,json.writeValueAsString(response));return response;
}
@GetMapping("/meals/{id}") public Object get(@AuthenticationPrincipal Jwt jwt,@PathVariable UUID id)throws Exception{var rows=db.queryForList("SELECT * FROM meals WHERE id=? AND user_id=?",id,user(jwt));if(rows.isEmpty())throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Meal not found");return decode(rows.get(0));}
@DeleteMapping("/meals/{id}") @ResponseStatus(HttpStatus.NO_CONTENT) @Transactional public void delete(@AuthenticationPrincipal Jwt jwt,@PathVariable UUID id){UUID owner=user(jwt);db.queryForObject("SELECT id FROM users WHERE id=? FOR UPDATE",UUID.class,owner);if(db.update("DELETE FROM meals WHERE id=? AND user_id=?",id,owner)==0)throw new ResponseStatusException(HttpStatus.NOT_FOUND,"Meal not found");db.update("UPDATE meal_requests SET response_json='null' WHERE user_id=? AND meal_id=?",owner,id);}
@PatchMapping("/meals/{id}") @Transactional public Object edit(@AuthenticationPrincipal Jwt jwt,@PathVariable UUID id,@Valid @RequestBody Edit m)throws Exception{
 UUID owner=user(jwt);db.queryForObject("SELECT id FROM users WHERE id=? FOR UPDATE",UUID.class,owner);get(jwt,id);
 String snap=snapshot(m.foodId(),m.grams());int changed=db.update("UPDATE meals SET food_id=?,grams=?,meal_type=?,eaten_at=?,snapshot=?,version=version+1 WHERE id=? AND user_id=? AND version=?",m.foodId(),m.grams(),m.mealType(),timestamp(m.eatenAt()),snap,id,owner,m.version());
 if(changed==0)throw new ResponseStatusException(HttpStatus.CONFLICT,"This meal changed on another device. Refresh before editing.");return get(jwt,id);
}
@GetMapping("/meals/daily") public Object daily(@AuthenticationPrincipal Jwt jwt,@RequestParam LocalDate date,@RequestParam(defaultValue="Asia/Kolkata") String zone)throws Exception{return dailyFor(user(jwt),date,zone);}
public Map<String,Object> dailyFor(UUID owner,LocalDate date,String zone)throws Exception{ZoneId z=ZoneId.of(zone);var start=date.atStartOfDay(z).toOffsetDateTime();var end=date.plusDays(1).atStartOfDay(z).toOffsetDateTime();var rows=db.queryForList("SELECT * FROM meals WHERE user_id=? AND eaten_at>=? AND eaten_at<? ORDER BY eaten_at,id",owner,start,end);List<Map<String,Object>> result=new ArrayList<>(),nutrients=new ArrayList<>();for(var row:rows){result.add(decode(row));nutrients.add(json.convertValue(json.readTree(row.get("snapshot").toString()).get("nutrition"),new TypeReference<Map<String,Object>>(){}));}return Map.of("date",date,"zone",zone,"items",result,"summary",Nutrition.total(nutrients));}
}
