module Problem12 where

import           Data.Graph
import           Data.List
import qualified Data.Set   as Set

type NodeId = Int
data Line = Line NodeId [NodeId] deriving Show

parse :: String -> Line
parse xs = Line (read nodeId) parsedNeighbors
  where
    (nodeId:_:neighbors) = words xs
    parsedNeighbors = map read $ map (filter (/=',')) neighbors

buildEdges :: Line -> [Edge]
buildEdges (Line nodeId neighbors) = zip (repeat nodeId) neighbors

buildAllEdges :: [Line] -> [Edge]
buildAllEdges = concatMap buildEdges

--findAllGroups Set -> Int
-- findAllGroups


answer :: IO()
answer = do
  file <- readFile "input/Problem12.input"
  let ls = map parse $ lines file
  let g = buildG (0, 1999) $ buildAllEdges ls
  print $ length $ reachable g 0

  let all = Set.fromList $ map (Set.fromList . (reachable g)) (vertices g) :: Set.Set ( Set.Set Vertex )
  print $ Set.size all
