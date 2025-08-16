# ==============================================================================
#   Loose Diff Utility (v1.0)
# ------------------------------------------------------------------------------
#   작성자: [Your Name or Alias]
#   생성일: 2023-10-27
#
#   기능:
#   두 텍스트 파일의 내용을 비교하되, 파일 맨 끝에 있는 중요하지 않은
#   공백이나 줄바꿈 문자들(insignificant trailing whitespace)은 무시합니다.
#   이를 통해 코드의 기능에 영향을 주지 않는 사소한 차이로 인해
#   'diff' 유틸리티가 두 파일을 다르다고 판단하는 문제를 해결합니다.
# ==============================================================================

# sys 모듈은 커맨드라인(터미널)에서 스크립트를 실행할 때,
# 사용자가 입력한 인자(argument)들을 가져오기 위해 필요합니다. (e.g., 파일 경로)
import sys

# difflib 모듈은 파이썬 표준 라이브러리로, 두 텍스트 시퀀스(예: 파일 내용) 간의
# 차이점을 계산하고 사람이 읽기 좋은 형식(diff)으로 보여주는 강력한 도구입니다.
import difflib

def read_file_content_loosely(file_path: str) -> str | None:
    """
    지정된 경로의 파일을 읽어, 파일 맨 끝의 모든 공백과 줄바꿈을 제거하여 반환합니다.

    이것이 이 프로그램의 핵심 로직("Loose"의 의미)입니다.
    파일의 실제 내용은 그대로 두되, 비교를 위한 '데이터'만 정제합니다.

    Args:
        file_path (str): 읽어올 파일의 경로.

    Returns:
        str | None: 파일 읽기 성공 시, 끝 공백이 제거된 파일 내용을 문자열로 반환합니다.
                    실패 시(파일이 없거나 읽기 오류), None을 반환합니다.
    """
    try:
        # 'with open(...)' 구문은 파일을 안전하게 열고, 블록이 끝나면 자동으로 닫아줍니다.
        # encoding='utf-8'는 한글을 포함한 다양한 문자를 올바르게 처리하기 위함입니다.
        with open(file_path, 'r', encoding='utf-8') as f:
            # f.read(): 파일의 전체 내용을 하나의 큰 문자열로 읽어옵니다.
            # .rstrip(): 이 문자열의 맨 오른쪽(끝)에서부터 시작하여 모든 종류의
            #            공백 문자(스페이스, 탭, 줄바꿈 문자 \n, \r\n 등)를 제거합니다.
            return f.read().rstrip()
            
    # FileNotFoundError는 지정된 경로에 파일이 없을 때 발생하는 가장 흔한 오류입니다.
    # 사용자에게 어떤 파일이 문제인지 명확히 알려줍니다.
    except FileNotFoundError:
        print(f"Error: 파일을 찾을 수 없습니다 - '{file_path}'")
        return None
        
    # Exception은 위에서 명시한 오류 외에 발생할 수 있는 모든 예기치 않은 오류
    # (예: 읽기 권한 없음, 인코딩 문제 등)를 처리하는 안전장치입니다.
    except Exception as e:
        print(f"Error: 파일을 읽는 중 오류 발생 - '{file_path}': {e}")
        return None

def loose_diff(file1_path: str, file2_path: str):
    """
    두 파일을 '느슨하게(loosely)' 비교하고 그 결과를 출력합니다.

    '느슨하다'는 것은 파일 맨 끝의 모든 공백과 줄바꿈은 무시한다는 의미입니다.
    """
    # 사용자에게 어떤 파일들을 비교하고 있는지 명확하게 보여줍니다.
    print(f"--- Loose Diff ---------------------------------")
    print(f" a: {file1_path}")
    print(f" b: {file2_path}")
    print(f"----------------------------------------------")

    # 핵심 기능을 하는 헬퍼 함수를 호출하여 각 파일의 '정제된' 내용을 가져옵니다.
    content1 = read_file_content_loosely(file1_path)
    content2 = read_file_content_loosely(file2_path)

    # 두 파일 중 하나라도 읽기에 실패했다면(None 반환), 비교를 중단합니다.
    # 오류 메시지는 read_file_content_loosely 함수 내부에서 이미 출력되었습니다.
    if content1 is None or content2 is None:
        return

    # [가장 중요한 비교 로직]
    # 끝 공백이 모두 제거된 두 파일의 내용이 완전히 동일한지 확인합니다.
    if content1 == content2:
        print("✅ 파일이 실질적으로 동일합니다 (끝 공백/줄바꿈 무시).")
        return

    # 만약 위 조건에서 통과하지 못했다면, 파일 내용 자체에 차이가 있다는 의미입니다.
    # 이제 사용자에게 정확히 '어떤' 부분이 다른지 보여주기 위해 상세 diff를 생성합니다.
    print("\n⚠️  파일 내용에 차이가 있습니다:")
    
    # 상세 diff를 만들기 위해, 이미 정제된 내용을 다시 줄바꿈 단위로 나눕니다.
    # splitlines()는 \n, \r\n 등 다양한 줄바꿈 문자를 기준으로 문자열을 잘라 리스트로 만듭니다.
    lines1 = content1.splitlines()
    lines2 = content2.splitlines()

    # difflib.unified_diff는 Git diff와 유사한 형식의 '통합된(unified)' diff를 생성합니다.
    # 이 결과는 '제너레이터(generator)'이므로 for 루프를 통해 각 줄을 출력해야 합니다.
    diff = difflib.unified_diff(
        lines1,                      # 원본 파일 라인 리스트
        lines2,                      # 비교 대상 파일 라인 리스트
        fromfile=f'a/{file1_path}',  # diff 헤더에 표시될 원본 파일 이름
        tofile=f'b/{file2_path}',    # diff 헤더에 표시될 비교 대상 파일 이름
        lineterm=''                  # 각 diff 라인 끝에 불필요한 줄바꿈이 추가되는 것을 방지합니다.
    )

    # 생성된 diff 결과를 한 줄씩 화면에 출력합니다.
    for line in diff:
        print(line)

# `if __name__ == "__main__":` 블록은 이 스크립트 파일이 다른 파일에 'import' 되어서
# 사용될 때가 아닌, 터미널에서 `python loose_diff.py ...` 와 같이 직접 실행될 때만
# 내부 코드가 동작하도록 하는 파이썬의 표준적인 방법입니다.
if __name__ == "__main__":
    # sys.argv는 사용자가 터미널에서 입력한 모든 인자들을 담고 있는 리스트입니다.
    # sys.argv[0]은 항상 스크립트의 이름('loose_diff.py')입니다.
    # sys.argv[1]은 첫 번째 인자(파일1 경로), sys.argv[2]는 두 번째 인자(파일2 경로)가 됩니다.
    # 따라서 총 인자의 개수는 3개가 되어야 정상입니다.
    if len(sys.argv) != 3:
        print("사용법: python loose_diff.py <파일1_경로> <파일2_경로>")
        # sys.exit(1)은 프로그램이 오류와 함께 종료되었음을 운영체제에 알리는 표준적인 방법입니다.
        sys.exit(1)

    # 커맨드라인에서 받은 첫 번째와 두 번째 인자를 각각 변수에 저장합니다.
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    # 모든 준비가 끝났으므로, 메인 함수를 호출하여 비교를 시작합니다.
    loose_diff(file1, file2)