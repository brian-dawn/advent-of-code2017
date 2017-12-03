module Problem03 where

import           Control.Monad
import           Data.Array.IO
import           Data.List

circularize :: [a] -> [a]
circularize = concat . repeat

interleave :: [[a]] -> [a]
interleave = concat . transpose

repeatN :: a -> Int -> [a]
repeatN a amount = take amount $ repeat a

data Direction = U | L | R | D deriving (Show, Eq)
type Cartesian = (Int, Int)

directions :: [Direction]
directions = circularize [R, U, L, D]

-- lengths for this spiral are 1 1 2 2 3 3 etc.
distances :: [Int]
distances = interleave [[1..], [1..]]

steps :: [Direction]
steps = concat $ zipWith repeatN directions distances

origin :: Cartesian
origin = (0, 0)

step :: Direction -> Cartesian -> Cartesian
step direction (x, y) =
  case direction of
    U -> (x, y + 1)
    D -> (x, y - 1)
    R -> (x + 1, y)
    L -> (x - 1, y)

findCoord :: Int -> Cartesian
findCoord n = foldr step origin $ take (n-1) steps

solve :: Int -> Int
solve n = abs x + abs y
  where
    (x,y) = findCoord n


answer :: IO()
answer = do
  putStrLn "Problem03"
  print $ solve 289326
  answer2 <- solve2 289326
  print answer2


combinations :: [a] -> [b] -> [(a,b)]
combinations a b = (,) <$> a <*> b

type Grid = IOArray Cartesian Int

addCartesian :: Cartesian -> Cartesian -> Cartesian
addCartesian (x1,y1) (x2, y2) = (x1+x2, y1+y2)

selfAndNeighbors :: Cartesian -> [Cartesian]
selfAndNeighbors center = map (addCartesian center) $ combinations [-1..1] [-1..1]

sumSurrounding :: Cartesian -> Grid -> IO Int
sumSurrounding center array = do
  let neighbors = selfAndNeighbors center

  vals <- traverse (readArray array) neighbors

  return $ foldr1 (+) vals

walk2 :: Int -> Grid -> Cartesian -> [Direction] -> IO Int
walk2 target array location (direction:directions) = do
  sum <- sumSurrounding location array
  writeArray array location sum

  if sum > target then
    return sum
  else
    walk2 target array (step direction location) directions

solve2 :: Int -> IO Int
solve2 n = do
  -- Use problem 1 to help us.
  let (x, y) = findCoord n
  let finiteSteps = take (n-1) steps :: [Direction]

  let width = (abs x) + 3
  let height = (abs y) + 3

  let origin = (width `div` 2, height `div` 2) :: Cartesian

  array <- newArray ((0, 0), (width, height)) 0 :: IO Grid
  -- Start off at 1.
  writeArray array origin 1

  walk2 n array origin finiteSteps
