module Problem02 where

split = (map words) . lines

numbers :: (Num a, Read a) => [[String]] -> [[a]]
numbers = map (map read) -- unsafe use reads in real code

splitAndConvert = numbers . split

differenceBetweenMaxAndMin xs = maximum xs - minimum xs

checksum = sum . (map differenceBetweenMaxAndMin) . splitAndConvert
partOneAnswer = show . checksum

-- part 2

pairs []       = []
pairs (x:[])   = []
pairs (x:y:[]) = [(x,y)]
pairs (x:xs)   = [(x,y) | y <- xs] ++ (pairs xs)

largerFirst :: (Num a, Ord a) => (a,a) -> (a,a)
largerFirst (x,y) =
  if x > y
  then (x,y)
  else (y,x)

quotientsAndRemainders = (map (uncurry quotRem)) . (map largerFirst)

filterEvenlyDivisible = filter ((== 0) . snd)

checksum' = sum .
            (map
              -- the use of head here assumes that there will be an evenly divisible pair in each row
              -- and it will fail if there is not
              (fst . head . filterEvenlyDivisible . quotientsAndRemainders . pairs))
            . splitAndConvert

partTwoAnswer = show . checksum'
