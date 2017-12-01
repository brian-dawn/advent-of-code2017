#!/usr/bin/env ruby

input = ARGV[0]

def sum_duplicates(numbers, func)
  numbers.chars.each_with_index.select do |number, i|
    number == numbers[func.call(i)]
  end
    .map { |number, i| number.to_i }
    .reduce(:+)
end

# check against previous
get_previous_index = -> (x) { x - 1 }
puts sum_duplicates(input, get_previous_index)

# check against digit 'halfway around'
get_halfway_index = -> (x) { x - (input.length / 2) }
puts sum_duplicates(input, get_halfway_index)
