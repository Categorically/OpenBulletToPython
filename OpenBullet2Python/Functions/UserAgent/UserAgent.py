from enum import Enum
from random import randint, random, choice


# Credit for UserAgent class and random_window_version
# https://github.com/csharp-leaf/Leaf.xNet/blob/master/Leaf.xNet/~Http/Http.cs


class Browser(str, Enum):
    Chrome = "Chrome"
    Firefox = "Firefox"
    InternetExplorer = "InternetExplorer"
    Opera = "Opera"
    OperaMini = "OperaMini"


def random_window_version():

    windowsVersion = "Windows NT "
    random_number = randint(0,100)
    if random_number >= 1 and random_number <= 45:
        windowsVersion += "10.0"
    elif random_number > 45 and random_number <= 80:
        windowsVersion += "6.1"
    elif random_number > 80 and random_number <= 95:
        windowsVersion += "6.3"
    else:
         windowsVersion += "6.2"

    if random() <= 0.65:
        if random() <= 0.5:
            windowsVersion += "; WOW64"
        else:
            windowsVersion += "; Win64; x64"

    return windowsVersion
class UserAgent:
    def IEUserAgent():
        windowsVersion = random_window_version()
        version = None
        mozillaVersion = None
        trident = None
        otherParams = None

        if "NT 5.1" in windowsVersion:
            version = "9.0"
            mozillaVersion = "5.0"
            trident = "5.0"
            otherParams = ".NET CLR 2.0.50727; .NET CLR 3.5.30729"
        elif "NT 6.0" in windowsVersion:
            version = "9.0"
            mozillaVersion = "5.0"
            trident = "5.0"
            otherParams = ".NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.5.30729"
        else:
            random_number = randint(0, 2)

            if random_number == 0:
                version = "10.0"
                trident = "6.0"
                mozillaVersion = "5.0"

            elif random_number == 1:
                version = "10.6"
                trident = "6.0"
                mozillaVersion = "5.0"
            else:
                version = "11.0"
                trident = "7.0"
                mozillaVersion = "5.0"
            otherParams = ".NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E"

        return f"Mozilla/{mozillaVersion} (compatible; MSIE {version}; {windowsVersion}; Trident/{trident}; {otherParams})"

    def OperaUserAgent():
        version = None
        presto = None
        random_number = randint(0,3)
        if random_number == 0:
            version = "12.16"
            presto = "2.12.388"
        elif random_number == 1:
            version = "12.14"
            presto = "2.12.388"
        elif random_number == 2:
            version = "12.02"
            presto = "2.10.289"
        else:
            version = "12.00"
            presto = "2.10.181"

        return f"Opera/9.80 ({random_window_version()}); U) Presto/{presto} Version/{version}"

    def ChromeUserAgent():
        major = randint(62, 70);
        build = randint(2100, 3538);
        branchBuild = randint(0, 170)
        return f"Mozilla/5.0 ({random_window_version()}) AppleWebKit/537.36 (KHTML, like Gecko) " + f"Chrome/{major}.0.{build}.{branchBuild} Safari/537.36"

    def FirefoxUserAgent():
        FirefoxVersions = [64, 63, 62, 60, 58, 52, 51, 46, 45]
        version = choice(FirefoxVersions)
        return f"Mozilla/5.0 ({random_window_version()}; rv:{version}.0) Gecko/20100101 Firefox/{version}.0"

    def OperaMiniUserAgent():
        os = None
        miniVersion = None
        version = None
        presto = None

        random_number = randint(0, 2)
        if random_number == 0:
            os = "iOS"
            miniVersion = "7.0.73345"
            version = "11.62"
            presto = "2.10.229"
        elif random_number == 1:
            os = "J2ME/MIDP"
            miniVersion = "7.1.23511"
            version = "12.00"
            presto = "2.10.181"
        else:
            os = "Android"
            miniVersion = "7.5.54678"
            version = "12.02"
            presto = "2.10.289"

        return f"Opera/9.80 ({os}; Opera Mini/{miniVersion}/28.2555; U; ru) Presto/{presto} Version/{version}"

    def ForBrowser(browser):
        if browser == Browser.Chrome:
           return UserAgent.ChromeUserAgent() 
        elif browser == Browser.Firefox:
           return UserAgent.FirefoxUserAgent() 
        elif browser == Browser.InternetExplorer:
           return UserAgent.IEUserAgent()
        elif browser == Browser.Opera:
           return UserAgent.OperaUserAgent()
        elif browser == Browser.OperaMini:
           return UserAgent.OperaMiniUserAgent()
        else:
            return

    def Random():
        random_number = randint(0, 100)
        if random_number >= 1 and random_number <= 70:
            return UserAgent.ChromeUserAgent()
        if random_number > 70 and random_number <= 85:
            return UserAgent.FirefoxUserAgent()
        if random_number > 85 and random_number <= 91:
            return UserAgent.IEUserAgent()
        if random_number > 91 and random_number <= 96:
            return UserAgent.OperaUserAgent()
        
        return UserAgent.OperaMiniUserAgent()