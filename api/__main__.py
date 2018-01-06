try:
	from rank import get_rank_table, save
except:
	from .rank import get_rank_table, save

def main():
	get_rank_table()

if __name__ == '__main__':
	main()