# Product Requirements Document (PRD)

## Project
**Real-Time Document Scanner and Chromatic Verification Mark Extractor Using Planar Homography and Adaptive Image Segmentation**

- **Version:** 1.0
- **Status:** Proposed / not yet implemented
- **Platform:** Desktop (Windows-first; cross-platform where supported)
- **Primary stack:** Python 3.11/3.12, OpenCV, NumPy
- **Optional UI:** PySide6

## 1. Product summary
A desktop computer-vision application that detects a flat physical document in a live webcam stream, rectifies its perspective using a planar homography, produces a high-contrast scan, and extracts color-selected blue/red ink marks such as signatures and stamps. The application exposes a multi-view diagnostic dashboard and saves processed outputs.

The solution uses deterministic classical computer-vision algorithms, not deep learning. **Color extraction is not signature authentication or stamp authenticity verification.**

## 2. Problem statement
Capturing paper documents with a webcam often yields skewed geometry, uneven lighting, and distracting backgrounds. Users also need a way to isolate colored handwriting or stamps from printed black text for inspection. The proposed system combines document detection, geometric correction, local enhancement, and chromatic segmentation into one interactive workflow.

## 3. Goals and measurable success criteria
| Goal | Acceptance measure |
|---|---|
| Detect a document | Detect a plausible convex four-corner boundary on representative fully visible pages; record detection rate on a labeled test set |
| Rectify perspective | Produce an upright rectangular document with legible content and consistent corner ordering |
| Enhance scan | Export grayscale and adaptive-thresholded versions; evaluate readability across sample lighting conditions |
| Extract colored marks | Produce separate blue and red masks and extracted candidate images; evaluate pixel precision/recall on annotated samples |
| Support real-time interaction | Display live feed and diagnostic outputs; measure sustained FPS and end-to-end latency |
| Export outputs | Save original rectified image, enhanced scan, masks, and extracted marks with non-colliding filenames |
| Target performance | Aim for 30+ processed FPS on suitable hardware, but do not claim this until measured |

## 4. Users and use cases
**Primary users:** students, document-digitization demonstrators, administrative users who need quick visual inspection of color-selected document marks.

**Core use cases:**
1. Hold a paper document in front of a webcam and see its detected boundary.
2. Capture a corrected, upright digital scan.
3. Inspect a high-contrast scan with reduced uneven-lighting effects.
4. Inspect blue-ink signatures or red-ink stamp candidates in separate outputs.
5. Save the scan and extraction artifacts for later review.

## 5. Scope
### In scope (MVP)
- Live webcam capture and camera availability/error handling.
- Grayscale conversion, resizing, Gaussian blur; optional bilateral filtering.
- Canny edge detection, contour selection, convex quadrilateral approximation.
- Corner ordering, homography computation, perspective warping.
- Grayscale and adaptive threshold document enhancement.
- HSV segmentation for configurable blue and red hue ranges; morphological cleanup.
- Four-view diagnostic HUD using OpenCV windows initially.
- Capture/freeze, resume, save, export, quit controls.
- FPS/latency instrumentation and representative sample-based testing.

### Post-MVP
- PySide6 multi-pane desktop GUI with controls and worker thread.
- Temporal smoothing and short-lived tracking through brief occlusions.
- Interactive HSV calibration and per-camera presets.
- Automatic capture after stable detection.
- PDF export and batch scanning.

### Out of scope
- Cryptographic or forensic authenticity verification of signatures/stamps.
- OCR, handwriting recognition, document classification.
- Guaranteed recovery from severe occlusion or curled pages.
- Cloud storage, user accounts, and remote processing.
- Deep-learning inference or GPU requirements.

## 6. Functional requirements
| ID | Requirement | Priority | Acceptance criteria |
|---|---|---|---|
| FR-01 | Start and stop webcam capture | Must | Opens camera, reports failure, releases resources on exit |
| FR-02 | Preprocess video frames | Must | Produces appropriately sized grayscale/denoised frames |
| FR-03 | Detect document candidates | Must | Returns valid convex quadrilateral or explicit no-detection state |
| FR-04 | Display tracked boundary | Must | Overlays four corners and edges without corrupting source frame |
| FR-05 | Rectify document | Must | Maps ordered source corners to a valid rectangle via homography |
| FR-06 | Enhance document | Must | Produces color, grayscale, and adaptive-binary outputs |
| FR-07 | Segment blue ink | Must | Returns mask and color-preserving isolated candidate output |
| FR-08 | Segment red ink | Must | Handles red hue wrap-around with two hue intervals |
| FR-09 | Clean segmented masks | Must | Configurable morphological opening/closing; preserves fine strokes as far as practical |
| FR-10 | Display diagnostic views | Must | Live tracker, Canny edges, rectified scan, extracted marks |
| FR-11 | Capture/freeze and resume | Must | Snapshot stays fixed until resumed; camera lifecycle remains valid |
| FR-12 | Export outputs | Must | Saves images and masks with unique timestamp/ID and reports errors |
| FR-13 | Report processing metrics | Should | Shows FPS and/or frame-processing latency |
| FR-14 | Stabilize corners | Should | Reduces visible jitter on stationary documents |
| FR-15 | Provide adjustable HSV settings | Could | User can change hue/saturation/value bounds |

## 7. Non-functional requirements
- **Performance:** Optimize toward 30+ processed FPS; benchmark actual FPS and latency at documented resolution and hardware. At 30 FPS the nominal frame budget is ~33.3 ms, including processing overhead.
- **Reliability:** Missing/invalid contours, failed camera reads, invalid warp sizes, and export errors must not crash the application.
- **Modularity:** Separate capture, preprocessing, detection, rectification, enhancement, segmentation, UI, and orchestration.
- **Testability:** Core transformations should be callable on static images without a webcam.
- **Privacy:** Local processing by default; no uploads or cloud dependency.
- **Portability:** Prefer cross-platform OpenCV APIs; test on the primary development OS.
- **Maintainability:** Pin tested dependencies and provide setup and run instructions.

## 8. Processing architecture
```text
Webcam → Frame Capture → Resize/Preprocess → Canny + Contours
                                           ↓
                                   Four-Corner Detection
                                           ↓
                                   Corner Stabilization
                                           ↓
                                   Planar Homography
                                           ↓
                                    Rectified Color Image
                                      ↙             ↘
                         Grayscale + Adaptive       HSV Blue/Red Masks
                             Thresholding          + Morphology
                                      ↘             ↙
                              Dashboard + Export
```

**Failure handling:** If no valid quadrilateral is found, display the live feed and an explicit detection status; do not warp invalid points. For brief loss of detection, optional tracked corners may be used only while confidence remains acceptable.

## 9. User experience and controls
### MVP HUD
1. Live camera feed with boundary overlay and status.
2. Canny edge map.
3. Rectified document / enhanced scan.
4. Color-selected mark output / mask.

### Keyboard controls
| Key | Action |
|---|---|
| `S` | Save current rectified and enhanced scans |
| `E` | Export selected mark masks and extracted images |
| `C` | Capture/freeze current valid document |
| `R` | Resume live tracking |
| `Q` | Quit and release camera |

## 10. Outputs
```text
output/<capture-id>/
  rectified_color.png
  grayscale.png
  enhanced_scan.png
  blue_mask.png
  red_mask.png
  blue_marks.png
  red_marks.png
  metadata.json  # optional: timestamp, image dimensions, thresholds, metrics
```
All exported artifacts must be derived from the same frozen/captured document to avoid mismatched results.

## 11. Validation and test scenarios
- Plain printed document on contrasting background.
- Documents rotated and viewed at different angles.
- Different page sizes and aspect ratios.
- Shadows, bright/dim illumination, paper creases.
- Blue signature, red stamp, both, and neither.
- Blue printed graphics / red logos as false-positive controls.
- Cluttered backgrounds and partial hand occlusions.
- Camera unavailable/disconnected and unwritable output directory.

**Metrics:** document detection rate; corner reprojection/pixel error against annotated corners; segmentation precision, recall, F1/IoU against manually labeled masks; mean/median/p95 frame latency; sustained FPS; save success rate.

## 12. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Contours fail on low contrast or occluded boundaries | Contrast tuning, contour scoring, temporal smoothing, clear failure state |
| Corner order causes inverted or twisted warp | Dedicated ordering tests and convexity checks |
| Shadows remain after thresholding | Compare adaptive methods and tune neighborhood parameters; document limits |
| Colored logos/text appear in masks | Treat as candidates, add region/shape filters, avoid authenticity claims |
| Thin signature strokes disappear | Tune morphology, preserve raw mask, use high-resolution capture |
| 30 FPS not reached | Profile per stage, downsample detection, reduce redundant conversions |
| UI freezes | Separate capture/processing from PySide6 UI thread in post-MVP |

## 13. Dependencies and assumptions
- A working webcam and camera permission.
- Mostly planar paper documents with at least intermittently visible boundaries.
- Blue/red inks distinguishable from the page background in HSV space.
- Python 3.11 or 3.12 and tested compatible OpenCV/NumPy versions.

## 14. Release gates
- **MVP gate:** End-to-end capture, detect, rectify, enhance, extract, display, and save on representative documents.
- **Quality gate:** Documented tests and measured failure cases; no unhandled crashes in normal use.
- **Performance gate:** Measured FPS/latency with recorded hardware and resolution; disclose whether 30+ FPS target is met.
- **Delivery gate:** Reproducible installation, README, screenshots, demonstration, and version-controlled code.
