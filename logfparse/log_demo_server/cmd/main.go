package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {

	// TODO: move this to a config file or env.
	INPUT_LOG_FILE := "./stream_demo_data.txt"
	OUTPUT_LOG_FILE := "./stream_demo.log"

	readCountLimit := 3
	readCounter := 0
	blockDelay := 1200 * time.Millisecond

	inputLogFile, err := os.OpenFile(INPUT_LOG_FILE, os.O_RDONLY, 0644)
	check(err)
	defer inputLogFile.Close()

	outputLogFile, err := os.OpenFile(OUTPUT_LOG_FILE, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer outputLogFile.Close()

	var currentLogBlock strings.Builder
	isBlockStarted := false

	for {

		scanner := bufio.NewScanner(inputLogFile)

		for scanner.Scan() {
			line := scanner.Text()
			if strings.HasPrefix(line, "------") {
				if isBlockStarted {
					fmt.Fprintf(outputLogFile, "%s\n", currentLogBlock.String())
					fmt.Printf("%s\n", currentLogBlock.String())
					currentLogBlock.Reset()
					time.Sleep(blockDelay)
				}
				isBlockStarted = true
			}
			currentLogBlock.WriteString(line + "\n")
		}

		check(scanner.Err())

		readCounter++
		if readCounter >= readCountLimit {
			outputLogFile.Truncate(0)
			readCounter = 0
		}

		inputLogFile.Seek(0, 0)
	}

}
