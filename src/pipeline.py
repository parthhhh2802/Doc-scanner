from src.preprocessing import preprocess
from src.document_detector import detect_document
from src.perspective import rectify_document
from src.enhancement import enhance_document
from src.color_extractor import extract_color_marks

def process_pipeline(frame):
    gray, edges = preprocess(frame)
    corners = detect_document(edges)
    
    result = {
        'frame': frame,
        'edges': edges,
        'corners': corners,
        'warped': None,
        'gray': None,
        'binary': None,
        'blue_mask': None,
        'red_mask': None,
        'blue_marks': None,
        'red_marks': None
    }
    
    if corners is not None:
        warped = rectify_document(frame, corners)
        result['warped'] = warped
        
        enhanced_data = enhance_document(warped)
        result['gray'] = enhanced_data['gray']
        result['binary'] = enhanced_data['binary']
        
        color_data = extract_color_marks(warped)
        result['blue_mask'] = color_data['blue_mask']
        result['red_mask'] = color_data['red_mask']
        result['blue_marks'] = color_data['blue_marks']
        result['red_marks'] = color_data['red_marks']
        
    return result
