import cv2
import settings


def get_cam_frames(camera_port=0):
    cap = out = None

    try:
        cap = cv2.VideoCapture(camera_port)
        # Get the width and height of frame
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Be sure to use the lower case
        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (width, height))

    except Exception as e:
        print(e)

    return cap, out


if __name__ == '__main__':

    tracker_switcher = {
        'BOOSTING': cv2.TrackerBoosting_create(),
        'MIL': cv2.TrackerMIL_create(),
        'KCF': cv2.TrackerKCF_create(),
        'TLD': cv2.TrackerTLD_create(),
        'MEDIANFLOW': cv2.TrackerMedianFlow_create(),
        'CSRT': cv2.TrackerCSRT_create(),
        'MOSSE': cv2.TrackerMOSSE_create()
    }

    # Initialize the tracker with the configured type
    tracker = tracker_switcher[settings.TRACKER_TYPE]

    # Capture frame-by-frame
    cap, out = get_cam_frames()
    ok, frame = cap.read()
    
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    if frame is not None:
        bbox = cv2.selectROI("Image", grame, False, False)

        # Initialize tracker with first frame and bounding box
        ok = tracker.init(frame, bbox)

        while cap.isOpened():

            # Capture frame-by-frame
            ok, frame = get_cam_frames().read()
            if not ok:
                break

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok, bbox = tracker.update(frame)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

            # Draw bounding box
            if ok:
                # Tracking success
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            else:
                # Tracking failure
                cv2.putText(frame, "Tracking failure detected", (100, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

            # Display tracker type on frame
            cv2.putText(frame, settings.TRACKER_TYPE + " Tracker", (100, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display FPS on frame
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

            # Display result
            cv2.imshow("Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release everything if job is finished
    out.release()
    cap.release()
    cv2.destroyAllWindows()
