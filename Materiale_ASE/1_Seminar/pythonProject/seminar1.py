from time import sleep

print("Hello, World!")

def convert_temp(temperature, unit):
    if unit == 'C':
        fahrenheit = temperature * 1.8 + 32
        return f"Celsius: {temperature} is equal to {fahrenheit} Fahrenheit"
    elif unit == 'F':
        celsius = (temperature - 32) * 5/9
        return f"Fahrenheit {temperature} is equal to {celsius} Celsius"

print("Conver temperature testing:")
print(convert_temp(25, 'C'))
sleep(1)
print(convert_temp(77, 'F'))
