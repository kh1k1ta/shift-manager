"""
python scripts/check_db.py
を実行してDB接続・テーブルの確認ができます
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.database import engine, Worker
from sqlalchemy.orm import Session

def main():
    print("DB接続テスト中...")
    try:
        with Session(engine) as session:
            workers = session.query(Worker).all()
            print(f"✅ 接続成功！")
            print(f"登録スタッフ数: {len(workers)}人")
            for w in workers:
                print(f"  - {w.id}: {w.name}（時給 {w.hourly_wage}円）")
    except Exception as e:
        print(f"❌ 接続失敗: {e}")

if __name__ == "__main__":
    main()
