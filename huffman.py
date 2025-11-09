# Compression Algorithm

# In compression, we'll be encoding data in a more compact representation [the deliverable of this tool- a compressed .bin file]
# In decompression, we'll be decoding that representation back into its original form

import heapq
from collections import defaultdict
import os

# -----------------------
# Node for Huffman Tree
# -----------------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Comparator for priority queue (min-heap)
    def __lt__(self, other):
        return self.freq < other.freq


# -----------------------
# Huffman Coding Class
# -----------------------
class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # Step 1: Frequency of each character
    def _make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for char in text:
            frequency[char] += 1
        return frequency

    # Step 2: Build Heap
    def _build_heap(self, frequency):
        for key, value in frequency.items():
            node = Node(key, value)
            heapq.heappush(self.heap, node)

    # Step 3: Merge Nodes to Build Huffman Tree
    def _build_tree(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    # Step 4: Generate Huffman Codes
    def _build_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self._build_codes_helper(root.left, current_code + "0")
        self._build_codes_helper(root.right, current_code + "1")

    def _build_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self._build_codes_helper(root, current_code)

    # Step 5: Encode the Text
    def _get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    # Step 6: Pad Encoded Text to make it byte-aligned
    def _pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for _ in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    # Step 7: Convert to bytes
    def _get_byte_array(self, padded_encoded_text):
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    # Public Method: Compress
    def compress(self):
        filename, _ = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r') as file:
            text = file.read()
            text = text.rstrip()

        frequency = self._make_frequency_dict(text)
        self._build_heap(frequency)
        self._build_tree()
        self._build_codes()
        # =======   below is the moment of compression   ======= 
        encoded_text = self._get_encoded_text(text)  
        # =======   now "encoded_text" contains the compressed bit representation   =======  


        padded_encoded_text = self._pad_encoded_text(encoded_text)
        b = self._get_byte_array(padded_encoded_text)     # b = ([0, 27]) this array contains example decimal values of bytes
        
        with open(output_path, 'wb') as output:
            output.write(bytes(b))

        print("Compression complete. Compressed file:", output_path)
        return output_path   #  final deliverable the compression tool produces

    # Public Method: Decompress
    def decompress(self, input_path):
        filename, _ = os.path.splitext(input_path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file:
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        # Remove padding
        padded_info = bit_string[:8]
        extra_padding = int(padded_info, 2)

        bit_string = bit_string[8:]  
        encoded_text = bit_string[:-1 * extra_padding]

        # Decode text
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        with open(output_path, 'w') as output:
            output.write(decoded_text)

        print("Decompression complete. Decompressed file:", output_path)
        return output_path


## more simplified appraoch [alongwith remmoval of decompression logic] 



import heapq
from collections import defaultdict
import os

class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    def __init__(self, path):
        self.path = path
        self.codes = {}

    
    def _frequency_dict(self, text):
        freq = defaultdict(int)
        for ch in text:
            freq[ch] += 1
        return freq

    
    def _build_tree(self, freq):
        heap = [Node(ch, f) for ch, f in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            n1, n2 = heapq.heappop(heap), heapq.heappop(heap)
            merged = Node(None, n1.freq + n2.freq, n1, n2)
            heapq.heappush(heap, merged)
        return heap[0]

    
    def _generate_codes(self, node, current=""):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current
            return
        self._generate_codes(node.left, current + "0")
        self._generate_codes(node.right, current + "1")

    
    def _encode_text(self, text):
        return ''.join(self.codes[ch] for ch in text)

    
    def _pad_bits(self, bits):
        padding = 8 - len(bits) % 8
        bits += '0' * padding
        return f"{padding:08b}" + bits  

    
    def _to_bytearray(self, bits):
        return bytearray(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))

    def compress(self):
        
        filename, _ = os.path.splitext(self.path)
        output_path = filename + ".bin"

        with open(self.path, 'r') as f:
            text = f.read().rstrip()

        
        freq = self._frequency_dict(text)
        root = self._build_tree(freq)
        self._generate_codes(root)

        encoded = self._encode_text(text)
        padded = self._pad_bits(encoded)
        byte_array = self._to_bytearray(padded)

        
        with open(output_path, 'wb') as f:
            f.write(bytes(byte_array))

        print(f"Compression complete → {output_path}")
        return output_path

