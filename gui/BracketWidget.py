import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class BracketWindow(QWidget):
    def __init__(self, leftTeams, rightTeams):
        super().__init__()
        self.leftTeams = leftTeams
        self.rightTeams = rightTeams
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tournament Bracket - First Round')
        self.setGeometry(30, 100, 1400, 800)  # Adjusted the window size
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        font = QFont('Arial', 10)
        painter.setFont(font)

        """
        LEFT SIDE OF BRACKET
        """

        # Left side positions for the lines (4 matches)
        leftX = 100
        yStart = 100
        matchHeight = 100  # Space between each match
        lineLength = 200  # Length of horizontal lines

        # Store the midpoints for vertical connections
        left_midpoints = []

        # Draw 4 lines on the left side and connect pairs with vertical lines
        for i in range(4):
            yPos = yStart + i * matchHeight
            painter.drawLine(leftX, yPos, leftX + lineLength, yPos)  # Draw horizontal line

            # Display team names directly on the lines
            if i < len(self.leftTeams):
                textWidth = painter.fontMetrics().width(self.leftTeams[i])  # Calculate text width
                painter.drawText(leftX + (lineLength - textWidth) // 2, yPos - 10, self.leftTeams[i])  # Centered on line

            # For every pair, draw a vertical line connecting them
            if i % 2 == 1:  # This checks if 'i' is odd, so every second pair
                vertical_start_y = yStart + (i - 1) * matchHeight
                vertical_end_y = yPos
                painter.drawLine(leftX + lineLength, vertical_start_y, leftX + lineLength, vertical_end_y)  # Vertical line on the right

                # Draw horizontal line extending from the center of the vertical line
                mid_vertical_y = (vertical_start_y + vertical_end_y) // 2  # Calculate midpoint
                painter.drawLine(leftX + lineLength, mid_vertical_y, leftX + lineLength + 150, mid_vertical_y)  # Horizontal line from the center

                # Store the midpoints for connecting vertical lines
                left_midpoints.append(mid_vertical_y)

        # Draw connecting vertical lines for the left side
        for i in range(len(left_midpoints) - 1):
            painter.drawLine(leftX + lineLength + 150, left_midpoints[i], leftX + lineLength + 150, left_midpoints[i + 1])  # Vertical connecting line

        """
        RIGHT SIDE OF BRACKET
        """
        # Right side positions for the lines (4 matches)
        rightX = 1100  # Moved the right lines further to the right
        right_midpoints = []

        
        # Draw 4 lines on the right side and connect pairs with vertical lines (on the left)
        for i in range(4):
            yPos = yStart + i * matchHeight
            painter.drawLine(rightX, yPos, rightX + lineLength, yPos)  # Draw horizontal line

            # Display team names directly on the lines
            if i < len(self.rightTeams):
                textWidth = painter.fontMetrics().width(self.rightTeams[i])  # Calculate text width
                painter.drawText(rightX + (lineLength - textWidth) // 2, yPos - 10, self.rightTeams[i])  # Centered on line

            # For every pair, draw a vertical line connecting them
            if i % 2 == 1:
                vertical_start_y = yStart + (i - 1) * matchHeight
                vertical_end_y = yPos
                painter.drawLine(rightX, vertical_start_y, rightX, vertical_end_y)  # Vertical line on the left

                # Draw horizontal line extending from the center of the vertical line to the left
                mid_vertical_y = (vertical_start_y + vertical_end_y) // 2  # Calculate midpoint
                painter.drawLine(rightX, mid_vertical_y, rightX - 150, mid_vertical_y)  # Horizontal line from the center to the left

                # Store the midpoints for connecting vertical lines
                right_midpoints.append(mid_vertical_y)

        # Draw connecting vertical lines for the right side
        for i in range(len(right_midpoints) - 1):
            painter.drawLine(rightX - 150, right_midpoints[i], rightX - 150, right_midpoints[i + 1])  # Vertical connecting line

        # Draw the final horizontal line at the midpoint of the last vertical lines
        if left_midpoints and right_midpoints:
            # Calculate the y position for the final horizontal line as the midpoint between the last left and right vertical connections
            finalY = (left_midpoints[-1] + right_midpoints[-1]) // 2  # Position at the midpoint of the last vertical lines
            finalY -= 100
            painter.drawLine(leftX + lineLength + 150, finalY, rightX - 150, finalY)  # Final match line

        painter.end()






def main():
    app = QApplication(sys.argv)
    
    # Test with 8 teams (4 on the left, 4 on the right)
    leftTeams = ['Team A', 'Team B', 'Team C', 'Team D']
    rightTeams = ['Team E', 'Team F', 'Team G', 'Team H']
    
    # Create the BracketWindow with test team names
    window = BracketWindow(leftTeams, rightTeams)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
