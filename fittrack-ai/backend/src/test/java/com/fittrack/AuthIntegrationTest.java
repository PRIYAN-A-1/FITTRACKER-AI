package com.fittrack;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import com.fasterxml.jackson.databind.*;
import java.time.*;
import java.util.*;
import org.junit.jupiter.api.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest(
    properties = {
      "spring.datasource.url=jdbc:h2:mem:fittrack;MODE=PostgreSQL;DATABASE_TO_LOWER=TRUE;DB_CLOSE_DELAY=-1",
      "spring.datasource.username=sa",
      "spring.datasource.password=",
      "fittrack.jwt-secret=test-only-secret-do-not-use-in-production-123456789",
      "fittrack.catalog=/nonexistent-test-catalog"
    })
@AutoConfigureMockMvc
class AuthIntegrationTest {
  @Autowired MockMvc mvc;
  @Autowired ObjectMapper json;
  @Autowired JdbcTemplate db;

  JsonNode register() throws Exception {
    String email = UUID.randomUUID() + "@example.test";
    var result =
        mvc.perform(
                post("/api/v1/auth/register")
                    .contentType("application/json")
                    .content(
                        json.writeValueAsString(
                            Map.of(
                                "email",
                                email,
                                "password",
                                "Test-password-1234",
                                "displayName",
                                "Test only"))))
            .andExpect(status().isCreated())
            .andReturn();
    return json.readTree(result.getResponse().getContentAsString());
  }

  String access(JsonNode n) {
    return "Bearer " + n.get("accessToken").asText();
  }

  @Test
  void authenticationRequired() throws Exception {
    mvc.perform(get("/api/v1/users/me")).andExpect(status().isUnauthorized());
  }

  @Test
  void registerReturnsOwnProfile() throws Exception {
    var n = register();
    mvc.perform(get("/api/v1/users/me").header("Authorization", access(n)))
        .andExpect(status().isOk())
        .andExpect(jsonPath("$.display_name").value("Test only"))
        .andExpect(jsonPath("$.password_hash").doesNotExist());
  }

  @Test
  void rejectsShortPassword() throws Exception {
    mvc.perform(
            post("/api/v1/auth/register")
                .contentType("application/json")
                .content(
                    "{\"email\":\"x@example.test\",\"password\":\"short\",\"displayName\":\"x\"}"))
        .andExpect(status().isBadRequest());
  }

  @Test
  void reusedRefreshRevokesFamily() throws Exception {
    var n = register();
    String payload =
        json.writeValueAsString(Map.of("refreshToken", n.get("refreshToken").asText()));
    var fresh =
        mvc.perform(post("/api/v1/auth/refresh").contentType("application/json").content(payload))
            .andExpect(status().isOk())
            .andReturn();
    var next = json.readTree(fresh.getResponse().getContentAsString());
    mvc.perform(post("/api/v1/auth/refresh").contentType("application/json").content(payload))
        .andExpect(status().isUnauthorized());
    mvc.perform(get("/api/v1/users/me").header("Authorization", access(next)))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void logoutRevokesAccess() throws Exception {
    var n = register();
    mvc.perform(post("/api/v1/auth/logout").header("Authorization", access(n)))
        .andExpect(status().isNoContent());
    mvc.perform(get("/api/v1/users/me").header("Authorization", access(n)))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void deletionRevokesAccess() throws Exception {
    var n = register();
    mvc.perform(delete("/api/v1/users/me").header("Authorization", access(n)))
        .andExpect(status().isNoContent());
    mvc.perform(get("/api/v1/users/me").header("Authorization", access(n)))
        .andExpect(status().isUnauthorized());
  }

  @Test
  void foreignMealIsHidden() throws Exception {
    var a = register();
    var b = register();
    UUID id = UUID.randomUUID();
    db.update(
        "INSERT INTO foods(id,name,brand,source,source_url,license,verification,source_version)"
            + " VALUES('test:1','TEST FIXTURE','','test','local','TEST','test','1') ON CONFLICT DO"
            + " NOTHING");
    db.update(
        "INSERT INTO meals(id,user_id,food_id,grams,meal_type,eaten_at,idempotency_key,snapshot)"
            + " VALUES(?,?,?,?,?,?,?,?)",
        id,
        UUID.fromString(a.get("userId").asText()),
        "test:1",
        100,
        "lunch",
        OffsetDateTime.now(),
        UUID.randomUUID(),
        "{}");
    mvc.perform(get("/api/v1/meals/" + id).header("Authorization", access(b)))
        .andExpect(status().isNotFound());
    mvc.perform(delete("/api/v1/meals/" + id).header("Authorization", access(b)))
        .andExpect(status().isNotFound());
  }
}
