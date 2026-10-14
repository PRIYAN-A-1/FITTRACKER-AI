package com.fittrack.config;

import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.env.EnvironmentPostProcessor;
import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.core.env.MapPropertySource;

/**
 * Adapts Render's postgres:// DATABASE_URL to the JDBC properties expected by Spring Boot.
 * JDBC DATABASE_URL values are passed through unchanged.
 */
public final class RenderDatabaseUrlEnvironmentPostProcessor
    implements EnvironmentPostProcessor {

  private static final String DATABASE_URL = "DATABASE_URL";

  @Override
  public void postProcessEnvironment(ConfigurableEnvironment environment, SpringApplication application) {
    String configured = environment.getProperty(DATABASE_URL);
    if (configured == null || configured.isBlank()) {
      return;
    }

    if (configured.startsWith("jdbc:")) {
      return;
    }

    if (!configured.startsWith("postgres://") && !configured.startsWith("postgresql://")) {
      return;
    }

    URI uri = URI.create(configured);
    StringBuilder jdbcUrl = new StringBuilder("jdbc:postgresql://").append(uri.getHost());
    if (uri.getPort() >= 0) {
      jdbcUrl.append(':').append(uri.getPort());
    }
    if (uri.getPath() != null && !uri.getPath().isBlank()) {
      jdbcUrl.append(uri.getPath());
    }
    if (uri.getRawQuery() != null && !uri.getRawQuery().isBlank()) {
      jdbcUrl.append('?').append(uri.getRawQuery());
    }

    Map<String, Object> properties = new LinkedHashMap<>();
    properties.put("spring.datasource.url", jdbcUrl.toString());

    String userInfo = uri.getRawUserInfo();
    if (environment.getProperty("DATABASE_USER") == null && userInfo != null) {
      int separator = userInfo.indexOf(':');
      String rawUser = separator >= 0 ? userInfo.substring(0, separator) : userInfo;
      properties.put("spring.datasource.username", decode(rawUser));
      if (environment.getProperty("DATABASE_PASSWORD") == null && separator >= 0) {
        properties.put("spring.datasource.password", decode(userInfo.substring(separator + 1)));
      }
    }

    environment.getPropertySources().addFirst(
        new MapPropertySource("renderDatabaseUrl", properties));
  }

  private static String decode(String value) {
    return URLDecoder.decode(value, StandardCharsets.UTF_8);
  }
}
