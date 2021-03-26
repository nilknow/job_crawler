import csv
seemsGoodForMe=[41,143,188,273,]
if __name__ == "__main__":
    with open("job_detail.csv", "r") as f:
        with open("washed_job_details.csv", "w") as nf:
            reader = csv.reader(f)
            writer = csv.writer(nf, delimiter=",")
            counter = 0
            for i, r in enumerate(reader):
                if i == 0:
                    print(f"{i} {r}")
                if i == 41:
                    print(f"{i} {r}")
                yearOk = "8+" not in r[6] and "8+" not in r[5] and "8+" not in r[4] \
                         and "5+" not in r[6] and "5+" not in r[5] and "5+" not in r[4] \
                         and "6+" not in r[6] and "6+" not in r[5] and "6+" not in r[4] \
                         and "7+" not in r[6] and "7+" not in r[5] and "7+" not in r[4] \
                         and "3+" not in r[6] and "3+" not in r[5] and "3+" not in r[4] \
                         and "4+" not in r[6] and "4+" not in r[5] and "4+" not in r[4] \
                         and "2+" not in r[6] and "2+" not in r[5] and "2+" not in r[4] \
                         and "10+" not in r[6] and "10+" not in r[5] and "10+" not in r[4] \
                         and "2 years" not in r[6] \
                         and "3 years" not in r[6] \
                         and "5 years" not in r[6] \
                         and "10 years" not in r[6]
                notSenior="Senior" not in r[0]
                fullTimeJob = "Full-Time" in r[3]
                notAndroidRelated = "Android" not in r[6]
                notCloudRelated = "cloud" not in r[6] and "distributed systems" not in r[6]
                noEnglishRequired = "english" not in r[6] and "English" not in r[6]
                aiRelated = "NLP" not in r[6] and "machine learning" not in r[6]
                ignoreIndex = [20, 24, 25,50,60,64,70,73,95,99,117,141,202]
                if yearOk and fullTimeJob and notAndroidRelated and notCloudRelated and noEnglishRequired \
                        and aiRelated and notSenior and i not in ignoreIndex:
                    counter += 1
                    print(f"{counter} {i} {r}")
                    writer.writerow(r[1:2] + r[6:])
