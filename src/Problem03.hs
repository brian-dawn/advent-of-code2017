module Problem03 where

import Data.Array.MArray
import Data.Array.IO

-- 37 36 35 34 33 32 31
-- 38 17 16 15 14 13 30
-- 39 18  5  4  3 12 29
-- 40 19  6  1  2 11 28
-- 41 20  7  8  9 10 27
-- 42 21 22 23 24 25 26
-- 43 43 45 46 47 48 49

-- bottomRight = (2n + 1) ^ 2

-- 1r, 1u, 2l, 2d, 3r, 3u, 4l, 4d, 5r, 5u, ...

distances = concatMap (replicate 2) [1..]

up    = ( 0,  1)
down  = ( 0, -1)
left  = (-1,  0)
right = ( 1,  0)

directions = cycle [right, up, left, down]

-- compilier doesn't like `uncurry replicate` because our infinite list is full of Integers not Ints
-- this makes sense, but means we need to use fromIntegral
expand (distance, direction) = replicate (fromIntegral distance) direction

moveSequence = concatMap expand $ zip distances directions

addPair (x,y) (a,b) = (x + a, y + b)

positions = scanl addPair (0,0) moveSequence

nthPosition n = head $ drop (n - 1) positions

-- since we start at 0,0 the L1 distance is the sum of the absolute value of the coordinates of our ending position
distanceFromOrigin (x, y) = (abs x) + (abs y)

n = 325489
partOneAnswer = show $ distanceFromOrigin $ nthPosition n

neighbors location = map (addPair location) [up, down, left, right, (1,1), (1,-1), (-1, 1), (-1,-1)]

sumNeighbors location array = sum <$> traverse (readArray array) (neighbors location)

run :: [(Int, Int)] -> IOArray (Int,Int) Int -> IO (Int)
run (location:nextLocations) array = do
  sum <- sumNeighbors location array
  if sum > n
    then return sum
    else do writeArray array location sum
            run nextLocations array

update :: IO (String)
update = do
  memory <- newArray ((-100,-100),(100,100)) 0 :: IO (IOArray (Int,Int) Int)
  writeArray memory (0,0) 1
  show <$> run (tail positions) memory

partTwoAnswer = update
