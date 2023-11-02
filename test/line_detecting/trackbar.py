import cv2
import numpy as np

def nothing(x):
    pass

if __name__ == '__main__':
    cap = cv2.VideoCapture('/dev/video0')
    while(1):
        cv2.namedWindow('TrackBar')

        cv2.createTrackbar('H lower', 'TrackBar', 0, 255, nothing)
        cv2.createTrackbar('H upper', 'TrackBar', 0, 255, nothing)
        cv2.createTrackbar('S lower', 'TrackBar', 0, 255, nothing)
        cv2.createTrackbar('S upper', 'TrackBar', 0, 255, nothing)
        cv2.createTrackbar('V lower', 'TrackBar', 0, 255, nothing)
        cv2.createTrackbar('V upper', 'TrackBar', 0, 255, nothing)

        while(1):
            # row, col = 1280, 720
            ret, color_image = cap.read()
            row, col = color_image.shape[:2]
            scale = 4
            r_row = int( row/scale )
            r_col = int( col/scale )
            color_image = cv2.resize( color_image, (r_col, r_row) )
            hsv_image = cv2.cvtColor( color_image, cv2.COLOR_BGR2HSV )
            if cv2.waitKey(1) & 0xFF == 27:
                # 0xFF means ESC key!
                break

            lower_h = cv2.getTrackbarPos('H lower','TrackBar')
            upper_h = cv2.getTrackbarPos('H upper','TrackBar')

            lower_s = cv2.getTrackbarPos('S lower','TrackBar')
            upper_s = cv2.getTrackbarPos('S upper','TrackBar')

            lower_v = cv2.getTrackbarPos('V lower','TrackBar')
            upper_v = cv2.getTrackbarPos('V upper','TrackBar')

            detect_color_lower = np.array( [lower_h, lower_s, lower_v], np.uint8 )
            detect_color_upper = np.array( [upper_h, upper_s, upper_v], np.uint8 )
            detect_color = cv2.inRange( hsv_image, detect_color_lower, detect_color_upper )

            mask_image = cv2.bitwise_and( hsv_image.copy(), hsv_image.copy(), mask=detect_color )
            mask_image = cv2.cvtColor(mask_image, cv2.COLOR_HSV2BGR)
            h_images = cv2.hconcat( [color_image, mask_image] )
            cv2.imshow('TrackBar', h_images)

    cv2.destroyAllWindows()
