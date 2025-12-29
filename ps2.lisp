(defun play-loop (strat0 strat1)
  (labels ((play-loop-iter (s0 s1 count history0 history1 limit)
             (cond ((= count limit) (print-out-results history0 history1 limit))
                   (t (let* ((result0 (funcall s0 history0 history1))
                             (result1 (funcall s1 history1 history0)))
                        (play-loop-iter s0 s1 (1+ count)
                                        (funcall *extend-history* result0 history0)
                                        (funcall *extend-history* result1 history1)
                                        limit))))))
    (play-loop-iter strat0 strat1 0
                    *the-empty-history*
                    *the-empty-history*
                    (+ 90 (random 21)))))

(defun print-out-results (history0 history1 number-of-games)
  (let ((scores (get-scores history0 history1)))
    (terpri)
    (format t "Player 1 Score:  ~A~%" (* 1.0 (/ (car scores) number-of-games)))
    (format t "Player 2 Score:  ~A~%" (* 1.0 (/ (cadr scores) number-of-games)))
    (terpri)))

(defun get-scores (history0 history1)
  (labels ((get-scores-helper (h0 h1 score0 score1)
             (cond ((funcall *empty-history?* h0) (list score0 score1))
                   (t (let* ((game (funcall *make-play* (funcall *most-recent-play* h0)
                                              (funcall *most-recent-play* h1)))
                             (new-score0 (+ (get-player-points 0 game) score0))
                             (new-score1 (+ (get-player-points 1 game) score1)))
                        (get-scores-helper (funcall *rest-of-plays* h0)
                                           (funcall *rest-of-plays* h1)
                                           new-score0
                                           new-score1))))))
    (get-scores-helper history0 history1 0 0)))

(defun get-player-points (num game)
  (nth num (get-point-list game)))

(defparameter *game-association-list*
  '(
   (("c" "c") (3 3))
   (("c" "d") (0 5))
   (("d" "c") (5 0))
   (("d" "d") (1 1))
   ))

(defun get-point-list (game)
  (cadr (extract-entry game *game-association-list*)))

(defun extract-entry (game alist)
  (cadr (assoc game alist :test #'equal))
  )

(defparameter *make-play* #'list)
(defparameter *the-empty-history* '())
(defparameter *extend-history* #'cons)
(defparameter *empty-history?* #'null)
(defparameter *most-recent-play* #'car)
(defparameter *rest-of-plays* #'cdr)

(defun NASTY (my-history other-history)
  "d")

(defun PATSY (my-history other-history)
  "c")

(defun SPASTIC (my-history other-history)
  (if (= (random 2) 0)
      "c"
      "d")
  )

(defun EGALITARIAN (my-history other-history)
  (labels ((count-instances-of (test hist)
            (cond ((funcall *empty-history?* hist) 0)
                  ((string= (funcall *most-recent-play* hist) test)
                   (1+ (count-instances-of
                                test
                                (funcall *rest-of-plays* hist))))
                  (t
                   (count-instances-of
                            test
                            (funcall *rest-of-plays* hist))))))
    (let ((ds (count-instances-of "d" other-history))
          (cs (count-instances-of "c" other-history)))
      (if (> ds cs)
          "d"
          "c"))))

(defun EYE-FOR-EYE (my-history other-history)
  (if (funcall *empty-history?* my-history)
      "c"
      (funcall *most-recent-play* other-history))
  )

; Testing extract-entry procedure
(print (extract-entry (list "d" "d") *game-association-list*))  ; -> (1 1)
(print (extract-entry (list "d" "c") *game-association-list*))  ; -> (5 0)
(print (extract-entry (list "c" "d") *game-association-list*))  ; -> (0 5)
(print (extract-entry (list "c" "c") *game-association-list*))  ; -> (3 3)
