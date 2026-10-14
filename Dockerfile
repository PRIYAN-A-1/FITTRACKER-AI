FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY fittrack-ai/backend/pom.xml .
COPY fittrack-ai/backend/src ./src
RUN mvn -B verify
RUN cp target/fittrack-api-*.jar /tmp/app.jar

FROM eclipse-temurin:21-jre
RUN useradd --system --uid 10001 app
WORKDIR /app
COPY --from=build /tmp/app.jar app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
