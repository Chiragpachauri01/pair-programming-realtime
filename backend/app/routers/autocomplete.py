from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="", tags=["autocomplete"])

class AutoReq(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

class AutoResp(BaseModel):
    suggestion: str
    replaceStart: int
    replaceEnd: int

@router.post("/autocomplete", response_model=AutoResp)
async def autocomplete(req: AutoReq):
    code = req.code[:req.cursorPosition]
    suggestion = ""
    replace_start = req.cursorPosition
    replace_end = req.cursorPosition

    if code.rstrip().endswith("def") or code.endswith("def "):
        suggestion = "function_name(args):\n    \"\"\"TODO: describe\"\"\"\n    pass"
    elif code.endswith("import "):
        suggestion = "sys, os, typing"
    elif code.endswith("print("):
        suggestion = "'')"
    else:
        import re
        m = re.search(r"(\w+)$", code)
        if m:
            word = m.group(1)
            suggestion = word + "_completed"
            replace_start = req.cursorPosition - len(word)
        else:
            suggestion = "# suggestion: continue typing"

    return {"suggestion": suggestion, "replaceStart": replace_start, "replaceEnd": replace_end}
