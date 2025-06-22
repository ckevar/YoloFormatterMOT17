def letterbox_sz(shape, expected_sz, stride):
    ratio = shape[1]/shape[0]
    
    new_hw = int(expected_sz / ratio)
    padding_pixels = int(expected_sz - new_hw)
    padding_pixels = padding_pixels % stride

    margin0 = int(padding_pixels / 2)
    margin1 = margin0 + (padding_pixels & 1)

    if ratio > 1:
        return (expected_sz, new_hw), margin0, margin1, 0, 0
    
    return (new_sz, expected_sz), 0, 0, margin0, margin1


