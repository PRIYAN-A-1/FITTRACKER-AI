package com.fittrack.nutrition;

import java.math.BigDecimal;
import java.util.*;

public final class Nutrition {
  public static final List<String> KEYS = List.of("calories", "protein", "carbs", "fat", "fiber");

  public static Map<String, Object> calculate(Map<String, Object> food, BigDecimal grams) {
    if (grams == null || grams.signum() <= 0 || grams.compareTo(new BigDecimal("5000")) > 0)
      throw new IllegalArgumentException("grams out of range");
    Map<String, Object> out = new LinkedHashMap<>();
    for (String key : KEYS) {
      Object value = food.get(key);
      out.put(
          key,
          value == null
              ? null
              : new BigDecimal(value.toString()).multiply(grams).divide(new BigDecimal("100")));
    }
    return out;
  }

  public static Map<String, Object> total(List<Map<String, Object>> rows) {
    Map<String, Object> out = new LinkedHashMap<>();
    for (String key : KEYS) {
      BigDecimal sum = BigDecimal.ZERO;
      boolean complete = true;
      for (var row : rows) {
        Object value = row.get(key);
        if (value == null) complete = false;
        else sum = sum.add(new BigDecimal(value.toString()));
      }
      Map<String, Object> item = new LinkedHashMap<>();
      item.put("knownSubtotal", sum);
      item.put("complete", complete);
      item.put("total", complete ? sum : null);
      out.put(key, item);
    }
    return out;
  }
}
