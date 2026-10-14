package com.fittrack.privacy;

import java.util.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users/me")
public class PrivacyController {
  final JdbcTemplate db;

  public PrivacyController(JdbcTemplate d) {
    db = d;
  }

  @GetMapping
  public Object profile(@AuthenticationPrincipal Jwt j) {
    return db.queryForMap(
        "SELECT id,email,display_name,time_zone,created_at FROM users WHERE id=?",
        UUID.fromString(j.getSubject()));
  }

  public record Profile(@jakarta.validation.constraints.NotBlank @jakarta.validation.constraints.Size(max=80) String displayName,@jakarta.validation.constraints.NotBlank @jakarta.validation.constraints.Size(max=80) String timeZone){}
  @PatchMapping public Object update(@AuthenticationPrincipal Jwt j,@jakarta.validation.Valid @RequestBody Profile p){java.time.ZoneId.of(p.timeZone());db.update("UPDATE users SET display_name=?,time_zone=? WHERE id=?",p.displayName(),p.timeZone(),UUID.fromString(j.getSubject()));return profile(j);}
  @GetMapping("/export")
  public Object export(@AuthenticationPrincipal Jwt j) {
    return Map.of(
        "profile",
        profile(j),
        "goals",db.queryForList("SELECT calories,protein,carbs,fat FROM nutrition_goals WHERE user_id=?",UUID.fromString(j.getSubject())),
        "requestHistory",db.queryForList("SELECT idempotency_key,meal_id,response_json FROM meal_requests WHERE user_id=?",UUID.fromString(j.getSubject())),
        "meals",
        db.queryForList(
            "SELECT * FROM meals WHERE user_id=? ORDER BY eaten_at",
            UUID.fromString(j.getSubject())));
  }

  @DeleteMapping
  @Transactional
  @ResponseStatus(org.springframework.http.HttpStatus.NO_CONTENT)
  public void delete(@AuthenticationPrincipal Jwt j) {
    db.update("DELETE FROM users WHERE id=?", UUID.fromString(j.getSubject()));
  }
}
