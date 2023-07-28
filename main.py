from enum import Enum
import sys, json
from utlis import *


class ReviewTimeline(Enum):
    TimelineHour12 = 12 * 3600
    # TimelineDayOne = 1 * 24 * 3600
    TimelineDayTwo = 2 * 24 * 3600
    TimelineDayFour = 4 * 24 * 3600
    TimelineDaySeven = 7 * 24 * 3600
    TimelineDayFifteen = 15 * 24 * 3600
    TimelineMonthOne = 30 * 24 * 3600
    TimelineMonthTwo = 60 * 24 * 3600
    TimelineMonthFour = 120 * 24 * 3600


REVIEW_TIMELINE = [
    ReviewTimeline.TimelineHour12,
    # ReviewTimeline.TimelineDayOne,
    ReviewTimeline.TimelineDayTwo,
    ReviewTimeline.TimelineDayFour,
    ReviewTimeline.TimelineDaySeven,
    ReviewTimeline.TimelineDayFifteen,
    ReviewTimeline.TimelineMonthOne,
    ReviewTimeline.TimelineMonthTwo,
    ReviewTimeline.TimelineMonthFour,
]
REVIEW_TIMELINE_KEYS = [
    "TimelineHour12",
    # "TimelineDayOne",
    "TimelineDayTwo",
    "TimelineDayFour",
    "TimelineDaySeven",
    "TimelineDayFifteen",
    "TimelineMonthOne",
    "TimelineMonthTwo",
    "TimelineMonthFour"
]

REVIEW_RECORDS = "review_records"
FIRST_LEARN_TIME = "first_learn_time"
LAST_LEARN_TIME = "last_learn_time"
TIMELINE = "review_time_line"

"""
[
    "id" : 1,
    'first_learn_time': '2023-03-02 10:00:11'
    "learn_status": {
        'review_records': [
            {
                "id" : 'TimelineHour12',
                'time': '2023-03-02 10:00:11'
            }
        ]
    }
    
]
"""


def record(content):
    contents = [s for s in content.split(",")]
    with open("records.json", "r") as file:
        results = []
        file_content = file.read()
        if file_content:
            results = json.loads(file_content)

        if content == "" or content == "all":
            contents = [r["id"] for r in results]

        for n in contents:
            n = int(n)

            result = {}
            for i, r in enumerate(results):
                if r["id"] != n:
                    continue

                result = r
                break

            if result:
                review_records = result.get(REVIEW_RECORDS)
                if review_records:
                    record = review_records[-1]
                    index = REVIEW_TIMELINE_KEYS.index(record["id"]) + 1
                else:  # 没有复习过但是学习过
                    index = 0
            else:  # 没有学习过
                index = -1

            if index == -1:  # 表示这个还没有复习过
                index = 0
                results.append(
                    {
                        "id": n,
                        FIRST_LEARN_TIME: get_utc8_now_datetimestr(),
                        REVIEW_RECORDS: [],
                    }
                )
                results.sort(key=lambda x: x["id"])
                continue

            if index < len(REVIEW_TIMELINE_KEYS):
                results[n - 1][REVIEW_RECORDS].append(
                    {
                        "id": REVIEW_TIMELINE_KEYS[index],
                        "time": get_utc8_now_datetimestr(),
                    }
                )

    with open("records.json", "w") as file:
        file.write(json.dumps(results))


def show_review_plan():
    plans = []
    with open("records.json", "r") as file:
        results = []
        file_content = file.read()
        if file_content:
            results = json.loads(file_content)

        now = datetime.now()
        for i, result in enumerate(results):
            first_learn_time = datetimestr_to_datetime(result[FIRST_LEARN_TIME])
            elapse_sec = (now - first_learn_time).total_seconds()

            if result.get(REVIEW_RECORDS):
                record = result[REVIEW_RECORDS][-1]
                j = REVIEW_TIMELINE_KEYS.index(record["id"])
            else:
                j = -1

            if j >= len(REVIEW_TIMELINE_KEYS) - 1:
                continue

            timeline = REVIEW_TIMELINE[j + 1]
            if elapse_sec >= timeline.value:
                plans.append(
                    {
                        "id": result["id"],
                        FIRST_LEARN_TIME: result[FIRST_LEARN_TIME],
                        LAST_LEARN_TIME: record["time"],
                        TIMELINE: REVIEW_TIMELINE_KEYS[j + 1],
                        "elapse_time": sec_to_regular_time(elapse_sec),
                    }
                )
                continue

    print("---------------------today review plan finished, check plan.json---------------------")
    with open("plans.json", "w", encoding="utf-8") as file:
        if plans:
            plans_txt = json.dumps(plans, ensure_ascii=False)
            file.write(plans_txt)


def main():
    argvs = sys.argv
    if argvs[1] == "record":
        record(argvs[2] if len(argvs) >= 3 else "all")
    elif argvs[1] == "show":
        show_review_plan()


if __name__ == "__main__":
    main()
