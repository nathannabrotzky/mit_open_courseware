(defvar const-gravity 9.8)
(defvar const-pi 3.14159)

(defun square (x) (* x x))

(defun bball-position (acceleration velocity position timestep)
  (+ position (* velocity timestep) (* (/ 1 2) acceleration (square timestep))))

(print (bball-position 0 0 0 0))     ; -> 0
(print (bball-position 0 0 20 0))    ; -> 20
(print (bball-position 0 5 10 10))   ; -> 60
(print (bball-position 2 2 2 2))     ; -> 10
(print (bball-position 5 5 5 5))     ; -> 185/2

(defun pyth-root1 (a b c)
  (/ (+ (* -1 b) (sqrt (- (square b) (* 4 a c)))) (* 2 a)))

(defun pyth-root2 (a b c)
  (/ (- (* -1 b) (sqrt (- (square b) (* 4 a c)))) (* 2 a)))

(print (pyth-root1 4 8 2))      ; -> -0.29289
(print (pyth-root2 4 8 2))      ; -> -1.70711
(print (pyth-root1 1 -4 4))     ; -> 2.0
(print (pyth-root2 1 -4 4))     ; -> 2.0

(defun time-to-impact (vertical-velocity elevation)
  (let ((counter 0))
    (loop while (> elevation 0)
           do (setq counter (+ counter 1))
           (setq elevation (
                            bball-position (* -1 const-gravity) vertical-velocity elevation counter 
                            ))
           )
    counter
   )
  )

(defun time-to-height (vertical-velocity elevation target-elevation)
  (let ((counter 0))
    (loop while (> elevation target-elevation)
           do (setq counter (+ counter 1))
           (setq elevation (
                            bball-position (* -1 const-gravity) vertical-velocity elevation counter
                            ))
           )
    counter
    )
  )

(defun degree2radian (deg)
  (/ (* deg const-pi) 180.))

(defun travel-distance-simple (elevation velocity angle)
  (* velocity (cos (degree2radian angle)) (time-to-impact (* velocity (sin (degree2radian angle))) elevation)))

(print (travel-distance-simple 3 30 30))
(print (travel-distance-simple 3 30 45))
(print (travel-distance-simple 3 30 60))
(print (travel-distance-simple 3 30 90))

(defvar alpha-increment 0.01)

(defun find-best-angle (velocity elevation)
  (let ((best-angle 0) (best-distance 0) (distance 0) (angle 0))
    (loop while (<= angle 90)
          do (setq angle (+ angle alpha-increment))
             (setq distance (travel-distance-simple elevation velocity angle))
             (if (> distance best-distance) (setq best-angle angle))
             (if (> distance best-distance) (setq best-distance distance))
          )
    best-angle
    )
  )

(print (find-best-angle 30 0.01)) ; -> ~ 45 degrees
(print (find-best-angle 60 0.01)) ; -> ~ 42 degrees
(print (find-best-angle 90 0.01)) ; -> ~ 45 degrees
(print (find-best-angle 60 6))    ; -> ~ 42 degrees

(defvar drag-coeff 0.5)
(defvar density 1.25)
(defvar mass 0.145)
(defvar diameter 0.074)
(defvar beta (* 0.5 drag-coeff density (* const-pi 0.25 (square diameter)))) ; beta * v^2 = drag

(defun travel-distance (velocity elevation angle)
  (let ((current-x 0) (current-y elevation) (current-u 0) (current-v 0) (current-speed 0))
    (setq current-u (* velocity (cos (degree2radian angle))))
    (setq current-v (* velocity (sin (degree2radian angle))))
    (setq current-speed (sqrt (+ (square current-u) (square current-v))))
    (loop while (> current-y 0)
          do (setq current-x (+ current-x (* current-u 0.01)))
             (setq current-y (+ current-y (* current-v 0.01)))
             (setq current-u (+ current-u (* -1 0.01 (/ 1 mass) current-speed beta current-u)))
             (setq current-v (+ current-v (* -1 0.01 (+ const-gravity (+ (/ 1 mass) current-speed beta current-v)))))
             (setq current-speed (sqrt (+ (square current-u) (square current-v)))))
    current-x
    )
  )

(print (travel-distance 45 3 45))   ; -> ~ 33.5 meters
(print (travel-distance 45 90 90))  ; -> ~ 0 meters

(defun find-throwing-angle (velocity elevation desired-distance)
  (let ((best-angle 0) (current-angle 0) (current-distance 0))
    (loop while (<= current-angle 90)
          do (setq current-distance (travel-distance velocity elevation current-angle))
             (if (> current-distance desired-distance) (if (= best-angle 0) (setq best-angle current-angle) (if (> best-angle current-angle) (setq best-angle current-angle))))
             (setq current-angle (+ current-angle 1))
          )
    best-angle
    )
  )

(print (find-throwing-angle 45 3 33))  ; -> 40 degrees
