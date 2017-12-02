#!/usr/bin/env ruby

require "csv"

filename = ARGV[0]

rows = CSV.open(filename, col_sep: "\t")
          .map { |row| row.map(&:to_i) }
diffs = rows.map { |row| row.max - row.min }
checksum = diffs.reduce(:+)

puts checksum

def even_val(row)
  row.each do |num|
    row.each do |other_num|
      next if other_num == num
      if num % other_num == 0
        return num / other_num
      end
    end
  end
  0
end

evens = rows.map { |row| even_val(row) }
checksum = evens.reduce(:+)

puts checksum
