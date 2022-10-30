package ru.alexgur.restservice;

import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.InputStream;
import tech.tablesaw.api.IntColumn;
import tech.tablesaw.api.StringColumn;
import tech.tablesaw.api.NumberColumn;
import tech.tablesaw.api.Table;
import tech.tablesaw.io.Source;
import tech.tablesaw.api.DoubleColumn;
import tech.tablesaw.api.StringColumn;
import tech.tablesaw.api.IntColumn;
import tech.tablesaw.columns.numbers.NumberColumnFormatter;
import tech.tablesaw.api.ColumnType;
import smile.data.formula.Formula;
import smile.classification.RandomForest;

// https://stackoverflow.com/questions/1988016/named-parameter-idiom-in-java

public class Predict {
    /* Для предсказания должны быть переданы в GET параметрах  
           Param Name        |         Type  |
    ------------------------------------------
                     Pclass  |      INTEGER  |
                        Sex  |       STRING  |
                        Age  |       DOUBLE  |
    Siblings_Spouses_Aboard  |      INTEGER  |
    Parents_Children_Aboard  |      INTEGER  |
                       Fare  |       DOUBLE  |
    */
    
    public final String error; // Описание ошибки, если она случилась.
    public int status; // Статус работы скрипта (0 = что-то сломалось: 1 = все хорошо).
    
    public int prediction; // Предсказание по выживанию пассажира (1 - выжил или 0 - умер).

    private final int Pclass;
    private final String Sex;
    private final double Age;
    private final int Siblings_Spouses_Aboard;
    private final int Parents_Children_Aboard;
    private final double Fare;
    
    public static class Builder {
        private String error = "";
        private int status = 1;
        
        private int Pclass;
        private String Sex;
        private double Age;
        private int Siblings_Spouses_Aboard;
        private int Parents_Children_Aboard;
        private double Fare;
        
        public Predict build() throws IOException, ClassNotFoundException {
            return new Predict(this);
        }

        public Builder setPclass(String Pclass) {
            if(Pclass == null){
                this.error = "Add GET param Pclass [INTEGER]";
                this.status = 0;
            }else{
                this.Pclass = Integer.parseInt( Pclass );
            }
            return this;
        }
        
        public Builder setSex(String Sex) {
            if(Sex == null){
                this.error = "Add GET param Sex [STRING]: male/female";
                this.status = 0;
            }else{
                this.Sex = Sex;
            }
            return this;
        }
        
        public Builder setAge(String Age) {
            if(Age == null){
                this.error = "Add GET param Age [DOUBLE]";
                this.status = 0;
            }else{
                this.Age = Double.parseDouble( Age );
            }
            return this;
        }
        
        public Builder setSiblings_Spouses_Aboard(String Siblings_Spouses_Aboard) {
            if(Siblings_Spouses_Aboard == null){
                this.error = "Add GET param Siblings_Spouses_Aboard [INTEGER]";
                this.status = 0;
            }else{
                this.Siblings_Spouses_Aboard = Integer.parseInt( Siblings_Spouses_Aboard );
            }
            return this;
        }
        
        public Builder setParents_Children_Aboard(String Parents_Children_Aboard) {
            if(Parents_Children_Aboard == null){
                this.error = "Add GET param Parents_Children_Aboard [INTEGER]";
                this.status = 0;
            }else{
                this.Parents_Children_Aboard = Integer.parseInt( Parents_Children_Aboard );
            }
            return this;
        }
        
        public Builder setFare(String Fare) {
            if(Fare == null){
                this.error = "Add GET param Fare [DOUBLE]";
                this.status = 0;
            }else{
                this.Fare = Double.parseDouble( Fare );
            }
            return this;
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    private Predict(Builder builder) throws IOException, ClassNotFoundException {
        Pclass = builder.Pclass;
        Sex = builder.Sex;
        Age = builder.Age;
        Siblings_Spouses_Aboard = builder.Siblings_Spouses_Aboard;
        Parents_Children_Aboard = builder.Parents_Children_Aboard;
        Fare = builder.Fare;
        status = builder.status;
        error = builder.error;
        
        if(status == 1){
            // Подготавливаем Данные, которые вводит пользователь для получения предсказания, чтобы создать таблицу tablesaw
            int[] ar_Pclass = { Pclass };
            String[] ar_Sex = { Sex  };
            double[] ar_Age = { Age };
            int[] ar_Siblings_Spouses_Aboard = { Siblings_Spouses_Aboard };
            int[] ar_Parents_Children_Aboard = { Parents_Children_Aboard };
            double[] ar_Fare = { Fare };

            Table tm = Table.create()
                .addColumns(IntColumn.create("Pclass", ar_Pclass))
                .addColumns(StringColumn.create("Sex", ar_Sex))
                .addColumns(DoubleColumn.create("Age", ar_Age))
                .addColumns(IntColumn.create("Siblings/Spouses Aboard", ar_Siblings_Spouses_Aboard))
                .addColumns(IntColumn.create("Parents/Children Aboard", ar_Parents_Children_Aboard))
                .addColumns(DoubleColumn.create("Fare", ar_Fare));
            // делаем те же самые преобразование с датасетом, что и при тренировке
            tm.replaceColumn("Sex", tm.stringColumn("Sex").asDoubleColumn().asIntColumn());

            // читаем модель из файла
            // AppController instance = new AppController();
            // InputStream fileIn = instance.getFileAsIOStream("t.smile.model.ser");
            // ObjectInputStream in = new ObjectInputStream(new BufferedInputStream(fileIn));
            // RandomForest model = (RandomForest) in.readObject();
            InputStream fileIn = this.getFileAsIOStream("models/titanic.smile.model.ser");
            ObjectInputStream in = new ObjectInputStream(new BufferedInputStream(fileIn));
            RandomForest model = (RandomForest) in.readObject();
            
            // Делаем предсказание
            int[] pred = model.predict(tm.smile().toDataFrame());

            prediction = pred[0];
        }
    }
    
    private InputStream getFileAsIOStream(final String fileName) 
    {
        InputStream ioStream = this.getClass()
            .getClassLoader()
            .getResourceAsStream(fileName);

        if (ioStream == null) {
            throw new IllegalArgumentException(fileName + " is not found");
        }
        return ioStream;
    }

    private void printFileContent(InputStream is) throws IOException 
    {
        try (InputStreamReader isr = new InputStreamReader(is); 
                BufferedReader br = new BufferedReader(isr);) 
        {
            String line;
            while ((line = br.readLine()) != null) {
                System.out.println(line);
            }
            is.close();
        }
    }
}