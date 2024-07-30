import pandas
# import fs
import os

def main(ROOT_DIR):
    df = pandas.read_csv(f"{ROOT_DIR}/metadata.csv", sep="|", header=None)

    df_two = pandas.DataFrame()

    for i, row in df.iterrows():
        print(row[0])

        if os.path.exists(f"{ROOT_DIR}/wavs/{row[0]}.wav"):
            df_two = pandas.concat([df_two, row.to_frame().T], ignore_index=True)
            # pandas.concat(df_two, row)
            # df_two.concat(row)
            # df_two.add(row)
            print("file exists")
        pass

    print(len(df), len(df_two))

    df_two.to_csv(f"{ROOT_DIR}/metadata.csv", sep="|", index=False, header=False)
    pass