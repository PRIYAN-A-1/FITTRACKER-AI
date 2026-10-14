package com.fittrack.auth;

import java.nio.charset.StandardCharsets;
import java.security.*;
import java.time.*;
import java.util.*;
import java.util.HexFormat;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.*;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class AuthService {
  final JdbcTemplate db;
  final PasswordEncoder passwords;
  final JwtEncoder encoder;
  final SecureRandom random = new SecureRandom();

  public AuthService(JdbcTemplate d, PasswordEncoder p, JwtEncoder e) {
    db = d;
    passwords = p;
    encoder = e;
  }

  String hash(String x) {
    try {
      return HexFormat.of()
          .formatHex(
              MessageDigest.getInstance("SHA-256").digest(x.getBytes(StandardCharsets.UTF_8)));
    } catch (Exception e) {
      throw new IllegalStateException(e);
    }
  }

  @Transactional
  public Map<String, Object> register(String email, String password, String name) {
    if (password.getBytes(StandardCharsets.UTF_8).length > 72)
      throw new IllegalArgumentException("Password exceeds 72 UTF-8 bytes");
    UUID id = UUID.randomUUID();
    db.update(
        "INSERT INTO users(id,email,password_hash,display_name) VALUES(?,?,?,?)",
        id,
        email.toLowerCase(Locale.ROOT).trim(),
        passwords.encode(password),
        name);
    return issue(id, UUID.randomUUID());
  }

  public Map<String, Object> login(String email, String password) {
    if (password.getBytes(StandardCharsets.UTF_8).length > 72)
      throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid credentials");
    var rows =
        db.queryForList(
            "SELECT id,password_hash FROM users WHERE email=?",
            email.toLowerCase(Locale.ROOT).trim());
    String dummy = "$2a$12$R9h/cIPz0gi.URNNX3kh2OPST9/PgBkqquzi.Ss7KIUgO2t0jWMUW";
    boolean ok =
        passwords.matches(
            password, rows.isEmpty() ? dummy : (String) rows.get(0).get("password_hash"));
    if (!ok || rows.isEmpty())
      throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid credentials");
    return issue((UUID) rows.get(0).get("id"), UUID.randomUUID());
  }

  Map<String, Object> issue(UUID id, UUID family) {
    byte[] b = new byte[32];
    random.nextBytes(b);
    String refresh = Base64.getUrlEncoder().withoutPadding().encodeToString(b);
    db.update(
        "INSERT INTO sessions(id,user_id,family,token_hash,expires_at) VALUES(?,?,?,?,?)",
        UUID.randomUUID(),
        id,
        family,
        hash(refresh),
        OffsetDateTime.now(ZoneOffset.UTC).plusDays(30));
    var claims =
        JwtClaimsSet.builder()
            .issuer("fittrack")
            .subject(id.toString())
            .claim("family", family.toString())
            .issuedAt(Instant.now())
            .expiresAt(Instant.now().plusSeconds(900))
            .build();
    String access =
        encoder
            .encode(JwtEncoderParameters.from(JwsHeader.with(MacAlgorithm.HS256).build(), claims))
            .getTokenValue();
    return Map.of("accessToken", access, "refreshToken", refresh, "expiresIn", 900, "userId", id);
  }

  // noRollbackFor commits family revocation when a reused token is detected.
  @Transactional(noRollbackFor = ResponseStatusException.class)
  public Map<String, Object> refresh(String token) {
    var rows = db.queryForList("SELECT * FROM sessions WHERE token_hash=? FOR UPDATE", hash(token));
    if (rows.isEmpty())
      throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid session");
    var r = rows.get(0);
    UUID family = (UUID) r.get("family");
    if (Boolean.TRUE.equals(r.get("revoked"))) {
      db.update("UPDATE sessions SET revoked=TRUE WHERE family=?", family);
      throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Session reused; sign in again");
    }
    var expiry =
        db.queryForObject(
            "SELECT expires_at FROM sessions WHERE id=?", OffsetDateTime.class, r.get("id"));
    if (expiry.isBefore(OffsetDateTime.now()))
      throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Session expired");
    db.update("UPDATE sessions SET revoked=TRUE WHERE id=?", r.get("id"));
    return issue((UUID) r.get("user_id"), family);
  }

  public void logout(UUID user) {
    db.update("UPDATE sessions SET revoked=TRUE WHERE user_id=?", user);
  }
}
