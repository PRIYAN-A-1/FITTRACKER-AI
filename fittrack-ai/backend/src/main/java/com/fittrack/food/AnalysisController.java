package com.fittrack.food;
import java.io.*;import java.net.URI;import java.net.http.*;import java.time.Duration;import javax.imageio.ImageIO;import javax.imageio.stream.ImageInputStream;import com.fasterxml.jackson.databind.*;import org.springframework.beans.factory.annotation.Value;import org.springframework.web.bind.annotation.*;import org.springframework.web.multipart.MultipartFile;import org.springframework.web.server.ResponseStatusException;import org.springframework.http.HttpStatus;
@RestController @RequestMapping("/api/v1/food") public class AnalysisController {
final String endpoint,token;final ObjectMapper json;final HttpClient client=HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
public AnalysisController(ObjectMapper j,@Value("${MODEL_SERVICE_URL:}")String e,@Value("${MODEL_SERVICE_TOKEN:}")String t){json=j;endpoint=e;token=t;}
@PostMapping(value="/analyze",consumes="multipart/form-data") public Object analyze(@RequestParam("image")MultipartFile image)throws Exception{
 if(image.isEmpty()||image.getSize()>8*1024*1024)throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Upload a JPEG or PNG of at most 8 MiB");byte[] bytes=image.getBytes();
 try(ImageInputStream input=ImageIO.createImageInputStream(new ByteArrayInputStream(bytes))){var readers=ImageIO.getImageReaders(input);if(!readers.hasNext())throw new IllegalArgumentException();var reader=readers.next();try{reader.setInput(input);String format=reader.getFormatName();if(!(format.equalsIgnoreCase("JPEG")||format.equalsIgnoreCase("PNG"))||(long)reader.getWidth(0)*reader.getHeight(0)>20_000_000)throw new IllegalArgumentException();}finally{reader.dispose();}}
 catch(Exception e){throw new ResponseStatusException(HttpStatus.BAD_REQUEST,"Invalid JPEG/PNG image");}
 if(endpoint.isBlank()||token.length()<32)throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Model service not configured. Use manual logging.");
 try{var request=HttpRequest.newBuilder(URI.create(endpoint+"/v1/analyze")).timeout(Duration.ofSeconds(20)).header("Authorization","Bearer "+token).header("Content-Type","application/octet-stream").POST(HttpRequest.BodyPublishers.ofByteArray(bytes)).build();var response=client.send(request,HttpResponse.BodyHandlers.ofString());if(response.statusCode()!=200)throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"No approved food model is available. Use manual logging.");var result=json.readTree(response.body());if(!result.has("modelVersion")||!result.path("candidates").isArray())throw new IOException("invalid model response");return result;}
 catch(InterruptedException e){Thread.currentThread().interrupt();throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Analysis interrupted. Use manual logging.");}catch(IOException e){throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,"Analysis service unavailable. Use manual logging.");}
}

}
