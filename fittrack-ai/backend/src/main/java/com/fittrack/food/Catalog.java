package com.fittrack.food;

import com.fasterxml.jackson.databind.*;
import java.math.BigDecimal;
import java.nio.file.*;
import java.util.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Component;

@Component
public class Catalog implements CommandLineRunner {
  final JdbcTemplate db;
  final ObjectMapper json;
  final String path;

  public Catalog(JdbcTemplate d, ObjectMapper j, @Value("${fittrack.catalog}") String p) {
    db = d;
    json = j;
    path = p;
  }

  @org.springframework.transaction.annotation.Transactional(rollbackFor=Exception.class)
  public void run(String... args) throws Exception {
    if (!Files.exists(Path.of(path))) {
      System.out.println("Catalog not present; run the data collector or USDA importer.");
      return;
    }
    try (var lines = Files.lines(Path.of(path))) {
      var iterator = lines.iterator();
      while (iterator.hasNext()) {
        var n = json.readTree(iterator.next());
        if (!"100g".equals(n.path("basis").asText()))
          throw new IllegalArgumentException("Unsupported catalog basis");
        db.update(
            "INSERT INTO"
                + " foods(id,name,brand,calories,protein,carbs,fat,fiber,source,source_url,license,verification,source_version)"
                + " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET"
                + " brand=EXCLUDED.brand,source=EXCLUDED.source,source_url=EXCLUDED.source_url,license=EXCLUDED.license,verification=EXCLUDED.verification,name=EXCLUDED.name,calories=EXCLUDED.calories,protein=EXCLUDED.protein,carbs=EXCLUDED.carbs,fat=EXCLUDED.fat,fiber=EXCLUDED.fiber,source_version=EXCLUDED.source_version",
            n.path("id").asText(),
            n.path("name").asText(),
            n.path("brand").asText(),
            num(n, "calories"),
            num(n, "protein"),
            num(n, "carbs"),
            num(n, "fat"),
            num(n, "fiber"),
            n.path("source").asText(),
            n.path("source_url").asText(),
            n.path("license").asText(),
            n.path("verification").asText(),
            n.path("source_version").asText());
      }
    }
  }

  BigDecimal num(JsonNode n, String k) {
    return n.path(k).isNumber() ? n.path(k).decimalValue() : null;
  }
}
