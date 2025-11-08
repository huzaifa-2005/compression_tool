# Huffman Coding - Time & Space Complexity Analysis

This section explains the **time and space complexity** of the Huffman Coding algorithm implemented in Python. We kept it simple and easy to understand.

---

## Time Complexity

Let **n** = total number of characters in the input text  
Let **k** = number of unique characters in the text  

**Compression Steps:**

1. **Count character frequency**: `O(n)`  
2. **Build min-heap**: `O(k log k)`  
3. **Build Huffman tree**: `O(k log k)`  
4. **Generate codes for characters**: `O(k)`  
5. **Encode text using codes**: `O(n)`  
6. **Convert bit string to bytes**: `O(n)`  

**Total Compression Time**:  
O(n + k log k)


**Decompression Steps:**

1. **Read compressed file and create bit string**: `O(n)`  
2. **Remove padding and decode bit string**: `O(n)`  

**Total Decompression Time**:  

O(n)


---

## Space Complexity

**Compression Space Usage:**

- Frequency dictionary: `O(k)`  
- Heap: `O(k)`  
- Huffman tree nodes: `O(k)`  
- Code mapping: `O(k)`  
- Encoded text (bit string): `O(n)`  
- Byte array: `O(n)`  

**Total Compression Space**:  

O(n + k)


**Decompression Space Usage:**

- Bit string from file: `O(n)`  
- Decoded text: `O(n)`  

**Total Decompression Space**:  

O(n)


---

**Summary Table**

| Step                     | Time Complexity     | Space Complexity |
|---------------------------|------------------|----------------|
| Frequency Dictionary      | O(n)             | O(k)           |
| Heap Building             | O(k log k)       | O(k)           |
| Huffman Tree Construction | O(k log k)       | O(k)           |
| Code Generation           | O(k)             | O(k)           |
| Encoding Text             | O(n)             | O(n)           |
| Padding & Byte Conversion | O(n)             | O(n)           |
| **Compression Total**     | O(n + k log k)   | O(n + k)       |
| **Decompression Total**   | O(n)             | O(n)           |




