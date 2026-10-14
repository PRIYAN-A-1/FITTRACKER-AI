package com.fittrack.security;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.*;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
@Order(-110)
public class RateLimit extends OncePerRequestFilter {
  record Window(long minute, int count) {}

  final Map<String, Window> windows = new HashMap<>();

  @Override
  protected void doFilterInternal(
      HttpServletRequest req, HttpServletResponse res, FilterChain chain)
      throws IOException, ServletException {
    String requestId = UUID.randomUUID().toString();
    res.setHeader("X-Request-ID", requestId);
    if (req.getRequestURI().equals("/actuator/health")) {
      chain.doFilter(req, res);
      return;
    }
    long now = System.currentTimeMillis() / 60000;
    boolean auth = req.getRequestURI().startsWith("/api/v1/auth/");
    String key = req.getRemoteAddr() + ":" + auth;
    boolean allowed;
    synchronized (windows) {
      windows.entrySet().removeIf(e -> e.getValue().minute() != now);
      Window v = windows.getOrDefault(key, new Window(now, 0));
      allowed = windows.size() < 10000 && v.count() < (auth ? 20 : 300);
      if (allowed) windows.put(key, new Window(now, v.count() + 1));
    }
    if (!allowed) {
      res.setStatus(429);
      res.setHeader("Retry-After", "60");
      res.setContentType("application/problem+json");
      res.getWriter()
          .write(
              "{\"type\":\"about:blank\",\"status\":429,\"title\":\"Too many"
                  + " requests\",\"detail\":\"Please retry in one minute\"}");
      return;
    }
    chain.doFilter(req, res);
  }
}
