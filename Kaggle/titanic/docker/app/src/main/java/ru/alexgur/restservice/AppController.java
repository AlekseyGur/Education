package ru.alexgur.restservice;

import java.util.Map;
import java.util.HashMap;
import java.io.IOException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

/* Проверка работы этого скрипта:

curl 'localhost:8080/predict?Pclass=2&Sex=female&Age=2&Siblings_Spouses_Aboard=2&Parents_Children_Aboard=2&Fare=2'
выдаёт 1

curl 'localhost:8080/predict?Pclass=3&Sex=male&Age=42&Siblings_Spouses_Aboard=2&Parents_Children_Aboard=2&Fare=2'
выдаёт 0
*/

/* Полезные ресурсы:
примеры создания restapi на spring:
https://spring.io/guides/gs/rest-service/

Как читать файлы из JAR в maven:
https://howtodoinjava.com/java/io/read-file-from-resources-folder/#22-complete-example
*/

@RestController
public class AppController {

	@RequestMapping(value="/predict", method = RequestMethod.GET)
    public Map<String, String> app(@RequestParam Map<String, String> params) throws IOException, ClassNotFoundException {
        /* Для предсказания должны быть переданы в GET параметрах  
               Param Name      
        -----------------------
                         Pclass
                            Sex
                            Age
        Siblings_Spouses_Aboard
        Parents_Children_Aboard
                           Fare
        */
        
        Predict prediction = Predict.builder()
                                    .setPclass( params.get("Pclass") )
                                    .setSex( params.get("Sex") )
                                    .setAge( params.get("Age") )
                                    .setSiblings_Spouses_Aboard( params.get("Siblings_Spouses_Aboard") )
                                    .setParents_Children_Aboard( params.get("Parents_Children_Aboard") )
                                    .setFare( params.get("Fare") )
                                    .build();
                    
        HashMap<String, String> result = new HashMap<>(); 
        if(prediction.error != ""){
            result.put("error", prediction.error);
        }
        result.put("status", String.valueOf(prediction.status) );
        result.put("value", String.valueOf(prediction.prediction) ); // 1 - выжил или 0 - умер
        return result;

	}
}
