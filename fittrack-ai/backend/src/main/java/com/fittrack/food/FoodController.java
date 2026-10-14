package com.fittrack.food;

import java.util.*;
import org.springframework.http.HttpStatus;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api/v1/food")
public class FoodController {
  final JdbcTemplate db;

  public FoodController(JdbcTemplate d) {
    db = d;
  }

  @GetMapping("/search")
  public Object search(
      @RequestParam(defaultValue = "") String q,
      @RequestParam(defaultValue = "0") int page,
      @RequestParam(defaultValue = "20") int size) {
    if (q.length() > 100 || page < 0 || page > 10000 || size < 1 || size > 100)
      throw new IllegalArgumentException();
    String pattern =
        "%"
            + q.toLowerCase(Locale.ROOT).replace("!", "!!").replace("%", "!%").replace("_", "!_")
            + "%";
    return Map.of(
        "items",
        db.queryForList(
            "SELECT * FROM foods WHERE LOWER(name) LIKE ? ESCAPE '!' ORDER BY name,id LIMIT ?"
                + " OFFSET ?",
            pattern,
            size,
            page * size),
        "page",
        page,
        "size",
        size,
        "total",
        db.queryForObject(
            "SELECT COUNT(*) FROM foods WHERE LOWER(name) LIKE ? ESCAPE '!'", Long.class, pattern));
  }

  @GetMapping("/{id}")
  public Object food(@PathVariable String id) {
    var rows = db.queryForList("SELECT * FROM foods WHERE id=?", id);
    if (rows.isEmpty()) throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Food not found");
    return rows.get(0);
  }

}
