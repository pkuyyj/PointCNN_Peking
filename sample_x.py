import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

def sample_x_distance(current_x_1, current_l_1, block_size, max_point_num):
    file_size = int(current_x_1.shape[0])
    num_size = int(current_x_1.shape[1])
    return_data = []
    return_label = []
    print(file_size)
    for i in range(file_size):
        print("This is",i)
        return_data_1 = []
        return_label_1 = []
        max_x, max_y, max_z = np.amax(current_x_1[i], axis=0)
        min_x, min_y, min_z = np.amin(current_x_1[i], axis=0)
        size_x = block_size
        delta_x = (max_x - min_x) / size_x
        delta_y = (max_y - min_y) / size_x
        h = list()
        for p in range(num_size):
            hx = np.floor((current_x_1[i][p][0] - min_x) / size_x)
            hy = np.floor((current_x_1[i][p][1] - min_y) / size_x)
            hz = np.floor((current_x_1[i][p][2] - min_z) / size_x)
            h.append(hx + hy * delta_x + hz * delta_x * delta_y)
        h = np.array(h)
        h_indices = np.argsort(h)
        h_sorted = h[h_indices]
        count = 0
        cnt = 0
        for q in range(len(h_sorted) - 1):
            if h_sorted[q] == h_sorted[q + 1]:
                continue
            else:
                point_idx = h_indices[count: q + 1]
                return_data_1.append(np.mean(current_x_1[i][point_idx], axis=0))
                return_label_1.append(current_l_1[i][point_idx[0]])
                count = q
                cnt = cnt + 1
                if cnt == max_point_num:
                    break
        while cnt < max_point_num:
            cnt = cnt + 1
            t = np.array([(max_x + min_x)//2, (max_y + min_y)//2, (max_z + min_z)//2])
            return_data_1.append(t)
            return_label_1.append(0)
        return_data.append(return_data_1)
        return_label.append(return_label_1)
        break

    return_data = np.array(return_data)
    return_label = np.array(return_label)
    print(return_data.shape[0])
    print("successful_generate")
    np.save(file="sample_train_data_total_1.npy", arr=return_data)
    np.save(file="sample_train_label_total_1.npy", arr=return_label)
    print("successful_save")

