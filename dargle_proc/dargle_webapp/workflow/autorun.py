import request, dargle_orm, sys

innie = sys.argv[1]
outie = sys.argv[2]
# thread_num = int(sys.argv[3])
domain = sys.argv[3]
header = sys.argv[4]
check = sys.argv[5]

request.line_count(innie)

if check == True:
    csv = request.process_links(innie,outie,header)
# For troubleshooting/skipping requests
else:
    csv = outie
dargle_orm.dbUpdate(csv,domain)
