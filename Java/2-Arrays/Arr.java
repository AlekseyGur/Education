// Компиляция
    // javac Arr.java
// Выполнение java
    // java Arr

public class Arr{
    public static void printArr(int[] arr){
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
    }

    public static void main(String args[]){
        Arr helper = new Arr();
        
        // Одномерные массивы примитивных типов
        int[] array1 = new int[5];
        
        System.out.println("Array size: " + array1.length);
        helper.printArr(array1);
        
        // Копирование массива
        // System.arraycopy(Object src, int srcPos, Object dest, int destPos, int length)
        int[] array2 = new int[5];
        System.arraycopy(array1, 0, array2, 0, array1.length);
        helper.printArr(array2);
        
        System.out.println( Arrays.equals(array1, array2) );
        System.out.println( Arrays.deepEquals(array1, array2) );

        int[] array3 = array1.clone();
        helper.printArr(array2);
    }
}
