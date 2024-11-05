import os
import pickle

class LZW:
    def __init__(self, path):
        self.path = path

    def compress(self):
        print("Compression processing")
        fileName, _ = os.path.splitext(self.path)
        outputPath = fileName + "+comprimido.bin"
        with open(self.path, 'r') as file, open(outputPath, 'wb') as output:
            text = file.read()
            compressed_data = self.__compress(text)
            pickle.dump(compressed_data, output)
        return outputPath

    def decompress(self, input_path):
        print("Decompression processing")
        fileName, _ = os.path.splitext(input_path)
        originalFileName, originalExtension = os.path.splitext(self.path)
        outputPath = fileName.replace("+comprimido", "+descomprimido") + originalExtension
        with open(input_path, 'rb') as file, open(outputPath, 'w') as output:
            compressed_data = pickle.load(file)
            uncompressed_data = self.__decompress(compressed_data)
            output.write(uncompressed_data)
        return outputPath

    def __compress(self, uncompressed):
        dict_size = 256
        dictionary = {chr(i): i for i in range(dict_size)}
        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                dictionary[wc] = dict_size
                dict_size += 1
                w = c
        if w:
            result.append(dictionary[w])
        return result

    def __decompress(self, compressed):
        dict_size = 256
        dictionary = {i: chr(i) for i in range(dict_size)}
        result = []
        w = chr(compressed.pop(0))
        result.append(w)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result.append(entry)
            dictionary[dict_size] = w + entry[0]
            dict_size += 1
            w = entry
        return ''.join(result)

if __name__ == "__main__":
    path = input("Enter path to your file!\n")
    lzw = LZW(path)
    compressedFile = lzw.compress()
    lzw.decompress(compressedFile)