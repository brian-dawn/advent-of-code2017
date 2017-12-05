module Problem05 where

import           Data.Array.IO

type Program = IOArray Int Int

convert :: String -> [Int]
convert =  map read . lines

example :: [Int]
example = [0, 3, 0, 1, -3 ]

inc :: Num a => a -> a
inc = (+1)

jump :: (Int -> Int) -> Int -> Int -> Program -> IO Int
jump instructionIncrementerFn numJumps n program = do
    bounds <- getBounds program
    instruction <- readArray program n
    if n < 0 || n >= snd bounds then
        return numJumps
    else do
        writeArray program n $ instructionIncrementerFn instruction
        jump instructionIncrementerFn
             (inc numJumps)
             (n+instruction)
             program


solve :: (Int -> Int) -> Program -> IO Int
solve instructionIncrementerFn = jump instructionIncrementerFn 0 0

answer :: IO()
answer = do
    putStrLn "Problem05"
    file <- readFile "input/Problem05.input"
    let instructions = convert file

    array <- newListArray (0, length instructions) instructions :: IO Program
    answer1 <- solve inc array

    print answer1

    array2 <- newListArray (0, length instructions) instructions :: IO Program
    answer2 <- solve (\a -> if a >= 3 then a-1 else a+1) array2
    print answer2
