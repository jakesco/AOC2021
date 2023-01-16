fmt:
	isort aoc/ && black aoc/

get-input:
	[ -n "$(day)" ] && \
	curl "https://adventofcode.com/2021/day/$(day)/input" \
		--header "Cookie: $$(cat .token)" > input.txt

.PHONY: get-input fmt
