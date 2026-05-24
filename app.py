import streamlit as st


# xây hàm lọc từ điển
def load_vocab ( file_path ):    #Tạo hàm tên load_vocab nhận vào tham số file_path
    with open ( file_path , 'r') as f:    # gán đối tượng trong file cho biến f
        lines = f. readlines ()   # biến lines là các dòng trong file được đọc => list gồm mỗi từ 1 dòng
        words = sorted (set ([ line . strip (). lower () for line in lines ]))
    processed_words = []
    for line in lines:
        p_line = line.strip().lower()   # loại bỏ khoảng trắng và ký tự và chuyển thành chữ thường
        processed_words.append(p_line)  # add từ đã xử lý vào list processed_words
        words = sorted(set(processed_words))    # set và sort từ
    return words
vocabs = load_vocab ( file_path ='./vocab.txt')

# tạo hàm tính khoảng cách levenshtein giữa 2 token                
def leven_distances(token1, token2):
    # Lấy độ dài của 2 chuỗi
    so_hang = len(token1) + 1
    so_cot = len(token2) + 1
    
    # Tạo ma trận rỗng
    leven_distances = []
    
    # Duyệt từng hàng để có số hàng là độ dài của token 1, còn số cột là độ dài của token 2
    for i in range(so_hang):
        # Tạo một hàng mới
        hang_moi = []
        
        # Duyệt từng cột trong hàng
        for j in range(so_cot):
            # Thêm số 0 vào hàng
            hang_moi.append(0)
        
        # Thêm hàng đã tạo vào ma trận
        leven_distances.append(hang_moi)
    
    # Trả về ma trận
    return leven_distances
    # điền giá trị cho hàng và cột 
    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if (token1[t1 - 1] == token2[t2 - 1]):
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if (a <= b and a <= c):
                    distances[t1][t2] = a + 1
                elif (b <= a and b <= c):
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


#Code đến giao diện của streamlit
def main():
    st.title("Word Correction using Levenshtein Distance")
    word = st.text_input("Word:")

    if st.button("Compute"):

        # compute levenshtein distance
        levenshtein_distances = dict()
        for vocab in vocabs:
            levenshtein_distances[vocab] = levenshtein_distance(word, vocab)

        # sorted by distance
        sorted_distences = dict(sorted(levenshtein_distances.items(), key=lambda item: item[1]))
        correct_word = list(sorted_distences.keys())[0]
        st.write("Correct word: ", correct_word)

        col1, col2 = st.columns(2)
        col1.write("Vocabulary:")
        col1.write(vocabs)

        col2.write("Distances:")
        col2.write(sorted_distences)

if __name__ == "__main__":
    main()