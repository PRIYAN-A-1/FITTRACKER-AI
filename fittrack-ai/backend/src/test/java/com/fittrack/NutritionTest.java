package com.fittrack;

import static org.junit.jupiter.api.Assertions.*;

import com.fittrack.nutrition.Nutrition;
import java.math.BigDecimal;
import java.util.*;
import org.junit.jupiter.api.Test;

class NutritionTest {
  @Test
  void scalesPrecisely() {
    assertEquals(
        new BigDecimal("12.345"),
        Nutrition.calculate(Map.of("protein", new BigDecimal("8.23")), new BigDecimal("150"))
            .get("protein"));
  }

  @Test
  void unknownStaysNull() {
    assertNull(Nutrition.calculate(Map.of(), BigDecimal.ONE).get("fat"));
  }

  @Test
  void zeroIsNotMissing() {
    assertEquals(
        BigDecimal.ZERO, Nutrition.calculate(Map.of("fat", 0), new BigDecimal("100")).get("fat"));
  }

  @Test
  void rejectsNegative() {
    assertThrows(
        IllegalArgumentException.class, () -> Nutrition.calculate(Map.of(), new BigDecimal("-1")));
  }

  @Test
  void incompleteTotalsStayUnknown() {
    var t = Nutrition.total(List.of(Map.of("protein", 5), Map.of()));
    assertNull(((Map<?, ?>) t.get("protein")).get("total"));
    assertEquals(new BigDecimal("5"), ((Map<?, ?>) t.get("protein")).get("knownSubtotal"));
  }
}
