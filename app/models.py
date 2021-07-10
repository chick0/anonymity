# salt
#   idx int
#   salt string 20
#   before datetime

# board
#   idx int
#   title string 32
#   content text maybe 65535
#

# reply
#   idx int
#   board_idx int
#   content string 500

# recommend
#   idx int
#   target_idx int
#   is_board tinyint [T: board, F: reply]
#   vote tinyint [T: Good, F: Bad]
