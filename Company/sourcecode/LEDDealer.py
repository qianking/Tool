import cv2
import numpy as np
from algorithm import closest_pair, calculate_distance

ledpath = r'D:\Qian\Codeing\Tool\LED\test photo\2367258900089_LED Green Bottom_20230628190650.jpg'
def Led_Selected(ledpath:str):
    """
    找出LED的輪廓並且框選出每顆LED燈
    1. 灰度化
    2. 膨脹腐蝕
    3. 演算法排列LED燈(由左至右，由上至下)
    4. 畫框選的圖案在圖像上
    5. 獲得可以框選的最小值和最大值
    Args:
        ledpath (str): LED照片的路徑

    Returns:
        1. image_copy (str): 處理過後的圖像 
        2. point_data (dict): 每顆LED的資料[name]:((center_X, center_Y), (w, h))
        3. selectable_length (tuple): 可框選的最大和最小值
    """
    image = cv2.imread(ledpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 51, 255, cv2.THRESH_BINARY)[1] #以大於51，小於255當作spec
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    # Step 2: Find contours
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Step 3: Extract points (x, y, w, h) from contours
    contour_data = [(x, y, w, h) for c in cnts for x, y, w, h in [cv2.boundingRect(c)]]
    # Step 4: Calculate max_side_length
    max_side_length = max([max(w, h) for x, y, w, h in contour_data])
    # Step 5: Sort contour data by y values and group them into rows
    sorted_contour_data_by_y = sorted(contour_data, key=lambda p: p[1])
    grouped_contour_data_by_diff = []
    current_row_data = [sorted_contour_data_by_y[0]]
    for i in range(1, len(sorted_contour_data_by_y)):
        if sorted_contour_data_by_y[i][1] - sorted_contour_data_by_y[i-1][1] <= max_side_length:
            current_row_data.append(sorted_contour_data_by_y[i])
        else:
            grouped_contour_data_by_diff.append(current_row_data)
            current_row_data = [sorted_contour_data_by_y[i]]
    grouped_contour_data_by_diff.append(current_row_data)

    # Step 6: Sort contour data within each row by x values
    sorted_rows_data_by_diff = [sorted(row, key=lambda p: p[0]) for row in grouped_contour_data_by_diff]
    final_sorted_points = [point for row in sorted_rows_data_by_diff for point in row]
    point_to_contour = {tuple(cv2.boundingRect(c)[:2]): c for c in cnts}
    point_data = {} #[name]:((center_X, center_Y), (w, h))
    # Step 7: Draw rectangles and annotate
    image_copy = np.copy(image)
    for i, (x, y, w, h) in enumerate(final_sorted_points):
        name = f"{i:02}"
        point_data[name] = ((x+(w//2), y+(h//2)),(w, h))
        cv2.rectangle(image_copy, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.putText(image_copy, name, (x, y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
        
    # Step 8: 計算LED最小的眶長度和最大的眶長度
    min_length = max_side_length
    max_length = closest_pair(list(point[0] for point in point_data.values())) #將中心點座標拿去找最近兩個點
    max_length = calculate_distance(max_length[0], max_length[1]) 
    selectable_length = (int(min_length), int(max_length))
    
    return image_copy, point_data, selectable_length

def Change_Selection_Length(ledpath:str, point_data:dict, select_length:int):
    image = cv2.imread(ledpath)
    leng = select_length // 2
    image_copy = np.copy(image)
    for name, point in point_data.items():
        cv2.rectangle(image_copy, (point[0][0]-leng, point[0][1]-leng), (point[0][0]+leng, point[0][1]+leng), (0, 0, 255), 1)
        cv2.putText(image_copy, name, (point[0][0]-leng, point[0][1]-leng - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
    return image_copy

def Find_Average_Hue(ledpath:str):
    """獲得該圖片V大於51的Hue平均值
    cv2.cvtColor獲得的HSV範圍為:
    H:0~180
    S:0~255
    V:0~255
    Args:
        ledpath (str): LED照片的路徑

    Returns:
        average_h_where_v_gt_50 (int): 平均Hue
    """
    image = cv2.imread(ledpath)
    # Find the average Hue value
    # Convert the original image to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # Extract the H and V channels
    h_channel = hsv_image[:, :, 0]
    v_channel = hsv_image[:, :, 2]

    # Create a mask where V > 50
    v_mask = v_channel > 51

    # Use the mask to select H values where V > 50
    selected_h_values = h_channel[v_mask]

    # Compute the average of selected H values
    average_h_where_v_gt_50 = np.mean(selected_h_values)

    # If you want to make sure the result is an integer
    average_h_where_v_gt_50 = int(average_h_where_v_gt_50)
    return average_h_where_v_gt_50


def LED_SpecCalculate(ledpath:str, point_data:dict, spec:list):
    """利用UI拿到的HSV spec來計算區域中的pass count，獲得led config

    Args:
        ledpath (str): led圖片的路徑
        point_data (dict): led的資料 [name]:((center_X, center_Y), (w, h)) 
        spec (list): UI使用者給的HSV spec

    Returns:
        config (dict): LED config
        led_result (list): 顯示給使用者的詳細資料，包含每個框選範圍的平均H、S、V，亮點的個數、通過spec的個數...等
    """
    passcount_range = 0.6

    config = dict()
    led_result = list()
    tmpconfig = {'CaseName':list(),
              'Location':list(),
              'SelectedLength':list(),
              'H_Upper':list(),
              'H_Lower':list(),
              'S_Upper':list(),
              'S_Lower':list(),
              'V_Upper':list(),
              'V_Lower':list(),
              'PASS_Count':list(),}
    
    image = cv2.imread(ledpath)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_light_range = np.array([0, 0, 51]) #用V大於50算出亮點個數
    upper_light_range = np.array([180, 255, 255])

    H_l = spec[0] - spec[1]
    H_u = spec[0] + spec[1]
    S_l = spec[2][0]
    S_u = spec[2][1]
    V_l = spec[3][0]
    V_u = spec[3][1]
    lower_spec_range = np.array([H_l//2, S_l, V_l]) #用拿到的led spec算出pass count
    upper_spec_range = np.array([H_u//2, S_u, V_u])


    for name, led in point_data.items():
        w = led[1][0]//2
        h = led[1][1]//2
        roi = img_hsv[led[0][1]-h : led[0][1]+h, led[0][0]-w : led[0][0]+w]

        mask_light_roi = cv2.inRange(roi, lower_light_range, upper_light_range)
        mask_spec_roi = cv2.inRange(roi, lower_spec_range, upper_spec_range)
        light_pixel_count = cv2.countNonZero(mask_light_roi)
        spec_pixel_count = cv2.countNonZero(mask_spec_roi)
        average_hsv = cv2.mean(roi, mask=mask_light_roi)[:3]

        PASS_Count = round(spec_pixel_count*passcount_range)
        tmpconfig['CaseName'].append(name)
        tmpconfig['Location'].append(f"{led[0][0]-w},{led[0][1]-h}")
        tmpconfig['SelectedLength'].append(f"{led[1][0]},{led[1][1]}")
        tmpconfig['H_Upper'].append(str(H_u))
        tmpconfig['H_Lower'].append(str(H_l))
        tmpconfig['S_Upper'].append(str(S_u))
        tmpconfig['S_Lower'].append(str(S_l))
        tmpconfig['V_Upper'].append(str(V_u))
        tmpconfig['V_Lower'].append(str(V_l))
        tmpconfig['PASS_Count'].append(str(PASS_Count))
        
        selection_area = led[1][0]*led[1][1]
        light_percentage = round((light_pixel_count / selection_area) *100)
        pass_percentage = round((spec_pixel_count / light_pixel_count) * 100)
    
        led_result.append((name, 
                           round(average_hsv[0]*2), 
                           round(average_hsv[1]), 
                           round(average_hsv[2]), 
                           selection_area, 
                           f"{light_pixel_count} ({light_percentage}%)", 
                           f"{spec_pixel_count} ({pass_percentage}%)",
                           PASS_Count))

    config['LED_Config'] = {key: ";".join(value) for key, value in tmpconfig.items()}
    return config, led_result


if "__main__" == __name__:
    Find_Average_Hue(r"D:\Qian\Codeing\Tool\LED\LEDTTool\test data\2367258900089_LED Green Bottom_20230628190650.jpg")