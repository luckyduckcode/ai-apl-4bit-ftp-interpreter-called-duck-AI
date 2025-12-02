from src.interpreter import APLInterpreter
import torch

def test_interpreter():
    interp = APLInterpreter()
    print(f"Device: {interp.device}")
    
    # Test 1: Iota
    res = interp.eval("⍳5")
    print(f"Test 1 (⍳5): {res}")
    assert isinstance(res, torch.Tensor)
    assert res.shape == (5,)
    
    # Test 2: Reshape
    res = interp.eval("2 3 ⍴ ⍳6")
    print(f"Test 2 (2 3 ⍴ ⍳6):\n{res}")
    assert res.shape == (2, 3)
    
    # Test 3: Assignment
    interp.eval("A <- 10")
    res = interp.eval("A")
    print(f"Test 3 (A): {res}")
    assert res == 10

if __name__ == "__main__":
    try:
        test_interpreter()
        print("All backend tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
