package classes;

import java.util.List;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.Random;
import java.util.Arrays;

public class Test {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.println("Enter the List Size : ");
        int size = Integer.parseInt(br.readLine());
        List<Integer> numbers = getList(size);
        // // List<Integer> sortedNumbers = getSortedList(numbers);
        // System.out.println("Attempts : ");
        // int attempts = Integer.parseInt(br.readLine());
        // List<Integer> rotatedList = rotateList(numbers, attempts);
        // System.out.println("Rotated List : " + rotatedList);
        // int[] arr = {0,1,0,3,12};
        // arr = shiftZero(arr);
        // System.out.println(Arrays.toString(arr));
        int[] arr = numbers.stream().mapToInt(i -> i).toArray();
        System.out.println(Arrays.toString(arr));
        arr = reverseArrayOfSubset(arr, 3, 7);
        System.out.println(Arrays.toString(arr));
    }

    static List<Integer> getList(int size) {
        Random rand = new Random();
        List<Integer> list = new ArrayList<>();

        for (int i = 0; i < size; i++) {

            int number = rand.nextInt(1, 10);
            // Below lines are for generating List without duplicates!
            // if (list.contains(number)) {
            // if (i != 0) {
            // i--;
            // }
            // continue;
            // }
            list.add(number);
        }
        System.out.println("Unsorted : " + list);
        return list;
    }

    static List<Integer> getSortedList(List<Integer> list) {
        Collections.sort(list);
        System.out.println("Sorted : " + list);
        return list;
    }

    static List<Integer> getMiss(List<Integer> list) {
        List<Integer> missing = new ArrayList<>();
        HashSet<Integer> missingSet = new HashSet<>();

        int min = list.get(0), max = list.get(list.size() - 1);
        for (int i = 0; i < list.size(); i++) {
            missingSet.add(list.get(i));
        }
        for (int i = min; i <= max; i++) {
            if (!missingSet.contains(i)) {
                missing.add(i);
            }
        }
        return missing;
    }
    static List<Integer> rotateList(List<Integer> list, int attempts) {
        for (int i = 0; i < attempts; i++) {
            Integer numToMove = list.remove(list.size() - 1);
            list.add(0, numToMove);
        }
        return list;
    }
    static int[] shiftZero(int[] arr) {
        int j = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] != 0 && arr[j] == 0) {
                swap(arr, i, j);
            }
            if (arr[j] != 0) {
                j++;
            }
        }
        return arr;
    }
    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    static int[] reverseArrayOfSubset(int[] arr, int ...args) {
        int start, end;
        if (args.length == 0) {
            start = 0;
            end = arr.length - 1;
        } else {
            start = args[0];
            end = args[1];
        }
        while (start < end) {
            swap(arr, start, end);
            start++;
            end--;
        }
        return arr;
    }
}


// 1, 1, 2, 4, 9 - 1
// 9, 1, 1, 2, 4 - 2
// 4, 9, 1, 1, 2 - 3
// 2, 4, 9, 1, 1 - 4
// 1, 2, 4, 9, 1 - 5
// 1, 1, 2, 4, 9 - 6