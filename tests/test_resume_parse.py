from tools.parse_resume import parse_resume


def test_parse_resume():
    # replace w actual path
    resume_path = "data/resume.docx"
    

    text = parse_resume(resume_path)

    assert isinstance(text, str)
    assert len(text.strip()) > 0

    print("Resume parsed successfully!")
    print(text[:1000])


if __name__ == "__main__":
    test_parse_resume()