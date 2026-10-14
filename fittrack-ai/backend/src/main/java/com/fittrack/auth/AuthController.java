package com.fittrack.auth;

import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import java.util.*;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
public class AuthController {
  final AuthService service;

  public AuthController(AuthService s) {
    service = s;
  }

  public record Register(
      @Email @NotBlank @Size(max = 254) String email,
      @NotBlank @Size(min = 12, max = 64) String password,
      @NotBlank @Size(max = 80) String displayName) {}

  public record Login(@Email @NotBlank String email, @NotBlank @Size(max = 64) String password) {}

  public record Refresh(@NotBlank @Size(max = 128) String refreshToken) {}

  @PostMapping("/register")
  @ResponseStatus(org.springframework.http.HttpStatus.CREATED)
  public Object register(@Valid @RequestBody Register r) {
    return service.register(r.email(), r.password(), r.displayName());
  }

  @PostMapping("/login")
  public Object login(@Valid @RequestBody Login r) {
    return service.login(r.email(), r.password());
  }

  @PostMapping("/refresh")
  public Object refresh(@Valid @RequestBody Refresh r) {
    return service.refresh(r.refreshToken());
  }

  @PostMapping("/logout")
  @ResponseStatus(org.springframework.http.HttpStatus.NO_CONTENT)
  public void logout(@AuthenticationPrincipal Jwt jwt) {
    service.logout(UUID.fromString(jwt.getSubject()));
  }
}
