from box_ai_agents_toolkit import (
    BoxClient,
    box_file_ai_ask,
    box_file_ai_extract,
    box_multi_file_ai_ask,
    box_multi_file_ai_extract,
)


def test_box_api_ai_ask(box_client: BoxClient):
    # HAB-1-01.docx = 1728677291168. This file must exists
    resp = box_file_ai_ask(
        box_client, "1728677291168", "what are the key point of this file"
    )
    assert resp is not None
    assert len(resp) > 0
    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp
    assert "HAB-1-01" in resp.get("answer")


def test_box_api_ai_extract(box_client: BoxClient):
    resp: dict = box_file_ai_extract(
        box_client,
        "1728677291168",
        "contract date, start date, end date, lessee name, lessee email, rent, property id",
    )
    assert resp is not None
    assert len(resp) > 0
    answer = resp.get("answer")
    # convert answer str to dict
    answer = eval(answer)
    assert isinstance(answer, dict)
    assert answer.get("contract date") is not None
    assert answer.get("start date") is not None
    assert answer.get("end date") is not None
    assert answer.get("lessee name") is not None
    assert answer.get("lessee email") is not None


def test_box_api_ai_ask_multi(box_client: BoxClient):
    file_ids = [
        "1823610366483",
        "1823610356883",
        "1823610359283",
        "1823610364083",
        "1823610368883",
    ]
    resp: dict = box_multi_file_ai_ask(
        box_client,
        file_ids,
        "what items where bought in these documents",
    )

    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp


def test_box_api_ai_extract_multi(box_client: BoxClient):
    file_ids = [
        "1728675448213",
        "1728675498613",
        "1728675455413",
    ]
    resp: dict = box_multi_file_ai_extract(
        box_client,
        file_ids,
        "contract date, start date, end date, lessee name, lessee email, rent, property id",
    )

    assert resp is not None
    assert len(resp) > 0
    assert isinstance(resp, dict)
    assert "answer" in resp
