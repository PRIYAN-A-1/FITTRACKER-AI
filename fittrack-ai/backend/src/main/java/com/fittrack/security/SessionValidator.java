package com.fittrack.security;

import java.util.UUID;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.oauth2.core.*;
import org.springframework.security.oauth2.jwt.Jwt;

public class SessionValidator implements OAuth2TokenValidator<Jwt> {
  final JdbcTemplate db;

  public SessionValidator(JdbcTemplate d) {
    db = d;
  }

  public OAuth2TokenValidatorResult validate(Jwt jwt) {
    try {
      Long count =
          db.queryForObject(
              "SELECT COUNT(*) FROM sessions WHERE user_id=? AND family=? AND revoked=FALSE AND"
                  + " expires_at>CURRENT_TIMESTAMP",
              Long.class,
              UUID.fromString(jwt.getSubject()),
              UUID.fromString(jwt.getClaimAsString("family")));
      if (count != null && count > 0) return OAuth2TokenValidatorResult.success();
    } catch (IllegalArgumentException e) {
    }
    return OAuth2TokenValidatorResult.failure(
        new OAuth2Error("invalid_token", "Session inactive", null));
  }
}
