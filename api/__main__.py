import argparse

try:
	from rank import get_rank_table, save
except:
	from .rank import get_rank_table, save

def main():
    argparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="fnGuide 유틸"
    )
    argparser.add_argument('-O', '--output', help='엑셀파일로 저장',  nargs='?')
    argparser.add_argument('-W', '--workers', type=int, help='최대스레드수',  nargs='?', default=10)
    args = argparser.parse_args()

    output_path = args.output
    max_worker = args.workers
    print('Starting with {} Workers...'.format(max_worker))

    df_rank = get_rank_table(max_worker=max_worker)

    if df_rank.empty:
        print('Cannot retrive ranking info')
    else:
        save(df_rank, output_path)


if __name__ == '__main__':
	main()